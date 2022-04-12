import cv2
import datetime
import time
import os
import boto3
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    print('Video uploaded....')
    return response


def video_remove_watermark(input_loc, output_loc):
    cap = cv2.VideoCapture(input_loc)
    fps = cap.get(cv2.CAP_PROP_FPS)
    totalNoFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)
    print("[INFO] Video Duration In Seconds: ", durationInSeconds, "s")
    x_end, x_start, y_end, y_start = 475, 7, 732, 115  # 0, 0, 0, 0
    getdatetime = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%p")
    # cv2.VideoWriter_fourcc(*'XVID')
    if os.path.exists(output_loc):
        full_path = f'{output_loc}/output{getdatetime}.avi'
    else:
        os.mkdir(output_loc)
        full_path = f'{output_loc}/output{getdatetime}.avi'

    frame_width = x_end - x_start
    frame_height = y_end - y_start

    size = (frame_width, frame_height)
    fps = int(round(cap.get(5)))
    if fps == 0:
        fps = 30
    output_movie = cv2.VideoWriter(full_path,
                                   cv2.VideoWriter_fourcc(*'MJPG'),
                                   fps, size)

    # cv2.VideoWriter(full_path, cv2.VideoWriter_fourcc(
    # *'XVID'), fps, (frame_width*2, frame_height), True)
    time_start = time.time()
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print("[INFO] Number of frames: ", video_length)
    print("[INFO] Removing Watermark..")
    try:
        while (True):
            ret, frame = cap.read()
            if ret == True:
                # 115 732 7 475
                crop = frame[y_start:y_end, x_start:x_end]
                output_movie.write(crop)
                cv2.imshow('Video', crop)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        pass
    try:
        if full_path:
            upload_file(f"{full_path}", 'my-bucket')
    except Exception as e:
        pass
    cap.release()
    # close all windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 1596944078622merged
    # 1597085044921merged
    # 1597093481287merged
    # 1597112663396merged
    # 45672561c7c07fd2d504528430e1548enavikour11_1594372379_musicallydowncom.mp4
    # enter the input video absolute path
    input_loc = '/home/alervice/Desktop/input_videos/video.mp4'
    # enter output location folder
    output_loc = '/home/alervice/Desktop/output_videos/'
    try:
        print("[START] The video Watermark removal started...")
        video_remove_watermark(input_loc, output_loc)
        print("[RESULT] The video was successfully saved...")
    except Exception as e:
        print("[FAILURE] Error occurs...", e)

