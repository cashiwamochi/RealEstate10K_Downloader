# RealEstate10K_downloader
These scripts are used to download RealEstate10K dataset. 

## How to use   
At first, you should download [RealEstate10K](https://google.github.io/realestate10k/download.html) and extract here manually.   
```shell
sh ./prepare.sh
python3 generate_dataset.py [test or train]
```
This downloads YouTube movies and extract frames which are needed.  Because of unkown reasons, `pytube` fails to download and save movies. 
In this case, sequence name is added to `failed_videos_{test, train}.txt`.   
Also, `vizualizer.py` is placed here. This shows us camera poses using Open3d.
```shell
python3 vizualizer.py [/path/to/pose_data.txt]
e.g. (python3 vizualizer.py ./RealEstate10K/test/0c4c5d5f751aabf5.txt)
```

RealEstate10K(including images) is very large. Please be careful.    
Pleaes use this at your own risk.
