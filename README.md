Code to replicate results from:

Cychosz, M., Edwards, J. R., Munson, B., Romeo, R. R., Kosie, J., & Newman, R. S. (*under review*). The everyday speech environments of preschoolers with and without cochlear implants. [10.31234/osf.io/kvzt4](https://psyarxiv.com/kvzt4)

# datasets

* `dataframes/CI_TH_matches.csv` - contains metadata for all children and audiological information for children with cochlear implants 

* `dataframes/icphs_speech.csv` - measures of the ambient speech environment (MAN & FAN) from LENA .its files

* `dataframes/icphs_voc_voc.csv` - child vocalization measures from LENA .its files

* `dataframes/icphs_ctc.csv` - conversational turn data from LENA .its files

* `dataframes/icphs_voc_its.csv` - basic metadata about each .its file

# scripts to process .its files
#### Note that these scripts were adapted from scripts also located in the [HomeBank Git Repo](https://github.com/HomeBankCode)

* `get_CHN_clips.py` - extract data about child vocalizations from LENA .its files (counts, intensity, timestamps, etc.)

* `get_its_info.py` - extract basic metadata such as child age and gender from LENA .its file preamble

* `get_speech_clips.py` - extract data about ambient speech from LENA .its files (FAN, FAF, MAN, OLN, etc.)

* `get_CTC_clips.py` - same as above, but to get counts of conversational turns

# modeling and scripts to replicate results

* `everyday_CI.Rmd` - main results markdown; also contains explanatory code to process .its files (but note that .its files are not shared publicly so that code chunk is for presentation purposes only)

* `supp_II.Rmd` - results markdown to successfully replicate results after removing the child who was implanted at 45 mos (outlier) 

# manuscript and figures

* `everyday_CI_Anon.pdf` - main manuscript including appendices with audiological information

* `supp_materialsI.pdf` - supplementary materials with additional information about household composition

* `supp_materialsII.pdf` - supplementary materials to replicate modeling results after removing child with activation age of 45 mos

* `figures/` - directory containing figures found in manuscript



