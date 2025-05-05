# Dataset Details for Multimodal Mind2Web Evaluation Splits: Cross-Task, Cross-Domain, and Cross-Website

<img src="m2w_tw.gif">

## Download Parsed Datasets from Hugging Face Hub

If you haven't already, install FiftyOne:

```bash
pip install -U fiftyone
```

## Usage

```python
import fiftyone as fo
from fiftyone.utils.huggingface import load_from_hub

# Load the cross-task dataset
cross_task = load_from_hub("Voxel51/mind2web_multimodal_test_task")

# Load the cross-domain dataset
cross_domain = load_from_hub("Voxel51/mind2web_multimodal_test_domain")

# Load the cross-website dataset
cross_domain = load_from_hub("Voxel51/mind2web_multimodal_test_website")
```

## Dataset Description
**Curated by:** The Ohio State University NLP Group (OSU-NLP-Group)  
**Shared by:** OSU-NLP-Group on Hugging Face  
**Language(s) (NLP):** en  
**License:** OPEN-RAIL License (mentioned in the Impact Statements section)

## Dataset Sources
**Repository:** https://github.com/OSU-NLP-Group/SeeAct and https://huggingface.co/datasets/osunlp/Multimodal-Mind2Web  
**Paper:** "GPT-4V(ision) is a Generalist Web Agent, if Grounded" by Boyuan Zheng, Boyu Gou, Jihyung Kil, Huan Sun, Yu Su  
**Demo:** https://osu-nlp-group.github.io/SeeAct

## Uses
### Direct Use
- Benchmarking web agents' generalization capabilities across different levels of difficulty
- Evaluating multimodal models on web navigation and interaction tasks
- Training and fine-tuning models for web navigation
- Testing various grounding strategies for web agents
- Comparing in-context learning vs. supervised fine-tuning approaches

### Out-of-Scope Use
- Developing web agents for harmful purposes (as stated in the paper's impact statement)
- Automating actions that could violate website terms of service
- Creating agents that access users' personal profiles or perform sensitive operations without consent

## Dataset Structure
The Multimodal Mind2Web dataset consists of three evaluation splits designed to test different aspects of generalization:

### Cross-Task Split
- **Purpose**: Evaluates generalization to new tasks on familiar websites and domains
- **Size**: 177 tasks across 17 domains and 64 websites
- **Complexity**: Tasks average 7.6 actions each
- **Statistics**: 4,172 avg. visual tokens, 607 avg. HTML elements, 123,274 avg. HTML tokens

### Cross-Website Split
- **Purpose**: Evaluates generalization to new websites within familiar domains
- **Size**: 142 tasks across 9 domains and 10 websites
- **Complexity**: Tasks average 7.2 actions each
- **Statistics**: 4,653 avg. visual tokens, 612 avg. HTML elements, 114,358 avg. HTML tokens

### Cross-Domain Split
- **Purpose**: Evaluates generalization to entirely new domains
- **Size**: 694 tasks across 13 domains and 53 websites
- **Complexity**: Tasks average 5.9 actions each
- **Statistics**: 4,314 avg. visual tokens, 494 avg. HTML elements, 91,163 avg. HTML tokens

## FiftyOne Dataset Structure

**Core Fields:**
- `action_uid`: StringField - Unique action identifier
- `annotation_id`: StringField - Annotation identifier
- `target_action_index`: IntField - Index of target action in sequence
- `ground_truth`: EmbeddedDocumentField(Detection) - Element to interact with:
  - `label`: Action type (TYPE, CLICK)
  - `bounding_box`: a list of relative bounding box coordinates in [0, 1] in the following format: `<top-left-x>, <top-left-y>, <width>, <height>]`
  - `target_action_reprs`: String representation of target action
- `website`: EmbeddedDocumentField(Classification) - Website name
- `domain`: EmbeddedDocumentField(Classification) - Website domain category
- `subdomain`: EmbeddedDocumentField(Classification) - Website subdomain category
- `task_description`: StringField - Natural language description of the task
- `full_sequence`: ListField(StringField) - Complete sequence of actions for the task
- `previous_actions`: ListField - Actions already performed in the sequence
- `current_action`: StringField - Action to be performed
- `alternative_candidates`: EmbeddedDocumentField(Detections) - Other possible elements

Each example across all splits includes:
- Task descriptions
- HTML structure
- Operations (CLICK, TYPE, SELECT)
- Target elements with attributes
- Action histories

## Dataset Creation
### Curation Rationale
The three splits were specifically designed to evaluate web agents' generalization capabilities at different levels of difficulty:
- **Cross-Task**: Tests adaptation to new tasks in familiar environments (easiest)
- **Cross-Website**: Tests adaptation to new websites within familiar domains (medium)
- **Cross-Domain**: Tests adaptation to entirely new domains (hardest)

This design allows for systematic evaluation of what makes web agent generalization challenging and which approaches work best in different scenarios.

### Source Data
#### Data Collection and Processing
- Based on the original MIND2WEB dataset
- Each HTML document is aligned with its corresponding webpage screenshot image
- Underwent human verification to confirm element visibility and correct rendering for action prediction
- Splits were carefully constructed to test specific generalization capabilities

#### Who are the source data producers?
Web screenshots and HTML were collected from:
- Cross-Task: 64 websites across 17 domains (all represented in training)
- Cross-Website: 10 new websites across 9 domains (domains represented in training)
- Cross-Domain: 53 websites across 13 domains (domains not represented in training)

### Annotations
#### Annotation process
Each task includes annotated action sequences showing the correct steps to complete the task. These were likely captured through a tool that records user actions on websites.

#### Who are the annotators?
Researchers from The Ohio State University NLP Group or hired annotators, though specific details aren't provided in the paper.

### Personal and Sensitive Information
The dataset focuses on non-login tasks to comply with user agreements and avoid privacy issues.

## Bias, Risks, and Limitations
- **Performance Patterns**: Different models show distinct patterns across splits:
  - Supervised fine-tuning methods perform better on Cross-Task
  - In-context learning with large models shows better generalization on Cross-Website and Cross-Domain
  - GPT-4V outperforms others by wider margins in more challenging settings
  
- **Complexity Variations**: Cross-Website has the most complex pages in terms of HTML elements and visual tokens
  
- **Task Distribution**: For online evaluation, the paper defines task difficulty categories:
  - Easy: 1-4 actions (37 tasks)
  - Medium: 5-9 actions (35 tasks)
  - Hard: 10-18 actions (18 tasks)
  
- **Practical Implications**: In-context learning appears more practical for true generalist web agents, while supervised fine-tuning remains competitive for specialized agents focused on specific websites
  
- **External Validity**: Website layouts and functionality may change over time, affecting the validity of the dataset

## Citation

GitHub: https://github.com/OSU-NLP-Group/SeeAct

```bibtex
@article{zheng2024seeact,
  title={GPT-4V(ision) is a Generalist Web Agent, if Grounded},
  author={Boyuan Zheng and Boyu Gou and Jihyung Kil and Huan Sun and Yu Su},
  booktitle={Forty-first International Conference on Machine Learning},
  year={2024},
  url={https://openreview.net/forum?id=piecKJ2DlB},
}

@inproceedings{deng2023mindweb,
  title={Mind2Web: Towards a Generalist Agent for the Web},
  author={Xiang Deng and Yu Gu and Boyuan Zheng and Shijie Chen and Samuel Stevens and Boshi Wang and Huan Sun and Yu Su},
  booktitle={Thirty-seventh Conference on Neural Information Processing Systems},
  year={2023},
  url={https://openreview.net/forum?id=kiYqbO3wqw}
}
```

### APA:
Zheng, B., Gou, B., Kil, J., Sun, H., & Su, Y. (2024). GPT-4V(ision) is a Generalist Web Agent, if Grounded. arXiv preprint arXiv:2401.01614.