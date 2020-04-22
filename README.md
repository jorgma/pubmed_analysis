### Main files:
#### 1. from pubmed.py

Used to get pmids from litcovid website, download articles info, e.g., title, authors.    

You should set **store_file_name** before usage. 
>Example: 

`store_file_name = 'data/covid19/'`  

If you want to download cited info from scratch,
you have to **delete cited_pmid.npy** manually. In general, you can leave other setting by default.

#### 1. search_pubmed.py
Used to get pmids from searching pubmed, download articles info, e.g., title, authors.  

You should set **store_file_name**. 
>Example: 

`store_file_name = 'data/sars/'`  

You should set search **term** by yourself. 
>Example:  
````
entrez_result = EntrezSearch(
    term='sars',
    mindate='2000',
    maxdate='2020',
    retmax=MAX_NUMBER_OF_ARTICLE,
    store_file_name=store_file_name,
    update=True
)
````
If you want to download cited info from scratch,
you have to **delete cited_pmid.npy** manually. In general, you can leave other setting by default.

### from_given_pmids.py

Download articles info with given pmids.

You should set **store_file_name**. 
>Example: 

`store_file_name = 'data/somewhere/'` 

You should specify **origin_pmid_list** by yourself. 
>Example:  
`origin_pmid_list = ['32303574', '32292814']`

### install dependency



**If you have any doubt, do not hesitate to contact me.**


