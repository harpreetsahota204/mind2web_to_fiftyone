# fiftyone_utils.py
import fiftyone as fo
import os
from PIL import Image
import json
import re

def add_prev_actions(example):
    """Add previous actions to each example in the dataset."""
    idx = int(example['target_action_index'])
    example['prev_actions'] = example['action_reprs'][:idx]
    return example

def prepare_dataset(dataset):
    """Prepare the HuggingFace dataset by adding necessary fields."""
    return dataset.map(add_prev_actions)

def create_detection(candidate_json, img_width, img_height, action_repr=None):
    """Create a FiftyOne Detection from a candidate JSON and image dimensions."""
    attributes = json.loads(candidate_json['attributes'])
    bbox_str = attributes['bounding_box_rect']
    x, y, width, height = map(float, bbox_str.split(','))
    
    if action_repr:
        action_type = action_repr.split('->')[1].split(':')[0].strip()
    else:
        action_type = candidate_json['tag']
    
    detection = fo.Detection(
        label=action_type,
        bounding_box=[
            x/img_width, y/img_height,
            width/img_width, height/img_height
        ]
    )
    
    if action_repr:
        detection.target_action_reprs = action_repr
        
    return detection

def clean_action_repr(action_repr):
    """Remove [...] pattern from action representation."""
    return re.sub(r'\[.*?\]\s*', '', action_repr)

def create_fiftyone_dataset(data, dataset_name, screenshots_dir, overwrite=True):
    """
    Create a FiftyOne dataset from Mind2Web data.
    
    Args:
        data: HuggingFace dataset containing Mind2Web data
        dataset_name (str): Name for the FiftyOne dataset
        screenshots_dir (str): Directory path to save screenshots
        overwrite (bool): Whether to overwrite existing dataset
    
    Returns:
        fo.Dataset: The created FiftyOne dataset
    """
    # Prepare the dataset first
    data = prepare_dataset(data)
    
    # Create the dataset
    dataset = fo.Dataset(dataset_name, overwrite=overwrite)

    samples = []
    for item in data:
        # Skip items without screenshots
        if item['screenshot'] is None:
            print(f"Skipping item {item['action_uid']} - no screenshot available")
            continue
            
        # Save PIL image to file
        img_filename = f"{item['action_uid']}.jpg"
        img_path = os.path.join(screenshots_dir, img_filename)
        os.makedirs(screenshots_dir, exist_ok=True)
        item['screenshot'].save(img_path)
        
        # Get image dimensions
        img_width, img_height = item['screenshot'].size
        
        # Create sample
        sample = fo.Sample(filepath=img_path)
        
        # Add core fields
        sample['action_uid'] = item['action_uid']
        sample['annotation_id'] = item['annotation_id']
        sample['target_action_index'] = int(item['target_action_index'])
        
        # Parse ground truth detection
        if item['pos_candidates']:
            gt_candidate = json.loads(item['pos_candidates'][0])
            sample['ground_truth'] = create_detection(
                gt_candidate, 
                img_width, 
                img_height, 
                item['target_action_reprs']
            )
        
        # Add classifications
        sample['website'] = fo.Classification(label=item['website'])
        sample['domain'] = fo.Classification(label=item['domain'])
        sample['subdomain'] = fo.Classification(label=item['subdomain'])
        
        # Add task description
        sample['task_description'] = item['confirmed_task']
        
        # Add sequence information
        sample['full_sequence'] = item['action_reprs']
        
        # Add previous actions
        sample['previous_actions'] = item['prev_actions']
        
        # Add clean current action
        sample['current_action'] = clean_action_repr(item['target_action_reprs'])
        
        # Add alternative candidates as a list of Detections
        sample['alternative_candidates'] = fo.Detections(detections=[
            create_detection(json.loads(cand), img_width, img_height)
            for cand in item['pos_candidates'][1:]
        ])
        
        samples.append(sample)

    if not samples:
        raise ValueError("No valid samples found in the dataset")

    # Add all samples at once
    dataset.add_samples(samples, dynamic=True)
    dataset.compute_metadata()

    # Create and save the sequences view
    view = dataset.group_by(
        "annotation_id",
        order_by="target_action_index"
    )
    dataset.save_view("sequences", view)
    
    # Save the dataset
    dataset.save()
    
    return dataset