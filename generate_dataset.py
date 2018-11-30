import os
import sys
import glob
import subprocess
import datetime

import cv2

from pytube import YouTube

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("usage: this.py [test or train]")
        quit()

    if sys.argv[1] == "test":
        mode = "test"
    elif sys.argv[1] == "train":
        mode = "train"
    else:
        print("invalid mode")
        quit()

    data_root = "./RealEstate10K/" + mode

    seqname_list = sorted(glob.glob(data_root + "/*.txt"))
    print("{} sequences are saved".format(len(seqname_list)))

    for txt_file in seqname_list:
        print("{} is the current target.".format(txt_file))

        dir_name = txt_file.split('/')[-1]
        dir_name = dir_name.split('.')[0]
        output_root = './videos/' + mode + '/' + dir_name

        if not os.path.exists(output_root):
            os.makedirs(output_root)
        else:
            continue

        seq_file = open(txt_file, "r")
        lines = seq_file.readlines()
        timestamp_list = []
        str_timestamp_list = []
        for idx, line in enumerate(lines):
            if idx == 0:
                youtube_url = line.strip()
            else:
                timestamp = int(line.split(' ')[0])
                str_timestamp_list.append(str(timestamp))
                timestamp = int(timestamp/1000) 
                str_hour = str(int(timestamp/3600000)).zfill(2)
                str_min = str(int(int(timestamp%3600000)/60000)).zfill(2)
                str_sec = str(int(int(int(timestamp%3600000)%60000)/1000)).zfill(2)
                str_mill = str(int(int(int(timestamp%3600000)%60000)%1000)).zfill(3)
                str_timestamp = str_hour+":"+str_min+":"+str_sec+"."+str_mill
                timestamp_list.append(str_timestamp)

        seq_file.close()
        print(datetime.datetime.now())
        try :
            # sometimes this fails because of known to issues of pytube and unknown factors
            yt = YouTube(youtube_url)
            stream = yt.streams.first()
            stream.download('./','current')
        except :
            failure_log = open('failed_videos_'+mode+'.txt', 'a')
            failure_log.writelines(txt_file+'\n')
            failure_log.close()
            continue

        videoname_candinate_list = glob.glob('./*')
        for videoname_candinate in videoname_candinate_list:
            print(videoname_candinate.split('.'))
            if videoname_candinate.split('.')[-2] == "/current":
                videoname = videoname_candinate

        # extract frames from a video
        for idx, timestamp in enumerate(timestamp_list):
            command = 'ffmpeg'+' -ss '+timestamp+' -i '+videoname+' -vframes 1 -f image2 '+output_root+'/'+str_timestamp_list[idx]+'.png'
            os.system(command)

        # remove videos
        command = "rm " + videoname 
        os.system(command)

        png_list = glob.glob(output_root+"/*.png")

        for pngname in png_list:
            img = cv2.imread(pngname, 1)
            img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
            cv2.imwrite(pngname, img)

        print("done!")
