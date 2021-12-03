
# pre: python3.6, pip3 reinstall 
# pip3 install boto3
# 

import boto3
import os
import time
from datetime import datetime

# 버킷 생성
def create_bucket(bucket):
    print("make new AWS S3 bucket " + bucket)
    bucket_info = s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'} # Seoul
    )

    return bucket_info

# 버킷으로 객체 업로드
def upload_object_to_bucket(filepath, extension, filename, bucket):
    print("upload to bucket about new ISSUE")

    # 텍스트 파일일시 
    if extension == '.txt':
        s3.upload_file(filepath + extension, bucket + '-text' , filename)

    # 이미지 파일일시
    elif extension == '.jpg' or extension == '.png' or extension == '.jpeg':
        s3.upload_file(filepath + extension, bucket + '-image' , filename)






if __name__ == "__main__":

    background_path = os.path.dirname(os.path.realpath(__file__)) # 현재 파일 경로
    issue_data_path = background_path + '/issue_data'
    issue_data_folder_list = os.listdir(issue_data_path)

    s3 = boto3.client(
        's3',  # aws s3
        aws_access_key_id="AKIA3WOVHZ7J4HHHO7OF",         # IAM access ID
        aws_secret_access_key="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"   # IAM secret key
    )

    bucket_response = s3.list_buckets()
    bucket_list = [bucket['Name'] for bucket in bucket_response['Buckets']] # 




    while True:
        print('no issue state')
        update_issue_folder = os.listdir(issue_data_path)
        target_bucket = ''



        if issue_data_folder_list != update_issue_folder:

            print("New Issue Occur!!")


            nowTime = int(datetime.today().strftime("%Y%m%d%H%M%S")) // 100
            check_bucket_target = str(nowTime)

            if check_bucket_target not in bucket_list:
                bucket_list.append(check_bucket_target)
                target_bucket = check_bucket_target
                create_bucket(check_bucket_target + '-image')
                create_bucket(check_bucket_target + '-text')

            
            new_issue_folders = [x for x in update_issue_folder if x not in issue_data_folder_list]


            for new_issue_folder in new_issue_folders:
                issue_data_folder_list.append(new_issue_folder)
                
                upload_object_list = os.listdir(issue_data_path + '/' + new_issue_folder )

                for upload_object in upload_object_list:
                    filepath,extension = os.path.splitext(issue_data_path + '/' + new_issue_folder + '/' + upload_object)
                    
                    upload_object_to_bucket(filepath, extension, upload_object, target_bucket)


            




        time.sleep(3)


    




