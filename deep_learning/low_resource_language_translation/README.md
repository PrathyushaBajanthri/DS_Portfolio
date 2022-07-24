# Low Resource Language Translation using Neural Machine Translation

This project concentrates on a niche topic of NLP: `Low Resource Language Translation`. As the word suggests, a language is considered as `Low Resource Language` when its online presence is considerably less. A Neural Machine Translation (NMT) system can produce better translations when it is developed using a large collection of parallel corpora. In the case, of High Resource Languages, with extensive data available in the digital format, it is comparatively easier to develop an NMT system that can perform at a state-of-the-art level.Whereas, in the case of a Low Resource Language, as the data in digital format is scarce the development of an NMT system with a state-of-the-art level requires more effort.Even though significant strides are made in Low Resource Language Translation, there is a minute gap that needs to be addressed in the case of Indian Languages.This project explores the development of an NMT system that can translate from a High Resource Language -English to a LowResource Language-Hindi. Also Finetuning, Domain Adaptation that allows the NMT system to translate data of a specific topic understanding the terminology of both source and target languages.

## Data Used

- EN-HI General Data: PM India Parallel Corpus (https://data.statmt.org/pmindia/)
- EN-HI Medical Domain Data: IIT Bombay Medical Corpus (https://www.cfilt.iitb.ac.in/iitb_parallel/)
- EN-HI Covid-19 Domain Data: Scrapped from NHS Inform COVID-19 guidelines (https://www.nhsinform.scot/translations/languages/hindi/)


## Some Information on the Notebooks
```
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
```

Please note only demo_models jupyter notebooks will work, the rest of the notebooks are for your reference.

1. data_preparation -> used to clean and pre-process the data
2. demo_models -> there are two notebooks, which can be opened in Jupyter and can be run cell by cell. All the necessary data will be downloaded by the notebook from my google drive. These notebooks have been tested and the outputs can be seen.
3. en_hi_experiments -> 3 notebooks for developing baseline, finetuned-1 (iitb) and finetuned-2 (iitb+nhs_inform) are provided.
4. evaluations -> two notebooks to evaluate the models with random samples which were analysed in the project are done using this notebook.
5. hi_en_experiments -> 3 notebooks for developing baseline, finetuned-1 (iitb) and finetuned-2 (iitb+nhs_inform) are provided.
6. IITB_medical_data_preparation -> 2 documents used to clean the marked IITB corpus are provided in this folder
7. plotting -> notebook used to generate plots which show the BLEU and PPL scores of the models during the training process.

Programming Language: Python3

Libraries: Pandas, Matplotlib, Seaborn, JoeyNMT, swifter
