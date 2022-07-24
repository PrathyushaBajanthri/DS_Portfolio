# Low Resource Language Translation using Neural Machine Translation

This case study focuses on a niche problem in NLP: `Low Resource Language Translation`. As the word suggests, a language can be considered a `Low Resource Language` when its online presence is considerably limited. This project targets to develop a Neural Machine Translation model using Transformers which can translate text from English a `High Resource Language` to Hindi a `Low Resource Language`. It also explores the concept of `Domain Adaptation` where a trained model is retrained using data of a specific domain to incorporate domain knowledge as well.


Please note that the uploaded zip folder will follow the below folder structure:

C:\HP\PYTHON\TO_UPLOAD\JUPYTER_NOTEBOOKS
├───data_preparation
│       data_preparation_full.ipynb
│
├───demo_models
│       demo_en_hi_domain_adapted_nmt.ipynb
│       demo_hi_en_domain_adapted_nmt.ipynb
│
├───en_hi_experiments
│       en_hi_baseline.ipynb
│       en_hi_in_domain_retrain.ipynb
│       en_hi_mixed_indomain_retrain.ipynb
│
├───evaluations
│       evaluation_en_hi_translations.ipynb
│       evaluation_hi_en_translations.ipynb
│
├───hi_en_experiments
│       hi_en_bt_baseline.ipynb
│       hi_en_bt_in_domain_retrain.ipynb
│       hi_en_bt_mixed_in_domain_retrain.ipynb
│
├───IITB_medical_data_preparation
│       domain_data_cleaning.ipynb
│       domain_data_prep.ipynb
│
└───plotting
        plots.ipynb

Please note only demo_models jupyter notebooks will work, the rest of the notebooks are for your reference.

- Data Preparation: This notebook is used to clean and pre-process the data
- Demo Models: There are two notebooks, which can be opened in Jupyter and can be run cell by cell. All the necessary data will be downloaded by the notebook from my google drive. These notebooks have been tested and the outputs can be seen.
- EN to HI Experiments: 3 notebooks for developing baseline, finetuned-1 (iitb) and finetuned-2 (iitb+nhs_inform) are provided.
- HI to EN experiments: 3 notebooks for developing baseline, finetuned-1 (iitb) and finetuned-2 (iitb+nhs_inform) are provided.
- Evaluations: Two notebooks to evaluate the models with random samples which were analysed in the thesis are done using this notebook.
- IITB Medical Data Preparation: 2 notebooks used to clean the marked IITB corpus are provided in this folder
- Plotting: This notebook is used to generate plots which show the BLEU and PPL scores of the models during the training process.
