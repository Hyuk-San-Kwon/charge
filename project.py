import os
import cv2
import time
import easyocr
import argparse

from sqlalchemy import true

from domain.user.user_crud import create_user, get_existing_user
from domain.user.user_schema import UserCreate
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends
from database import SessionLocal
from models import User
from speech import speak


def make_parser():
    parser = argparse.ArgumentParser("전기차 충전기-인터폰 제어 시스템")
    parser.add_argument(
        '-c', '--charge',  type=int, default=0, help='전기차 충전도 퍼센트'
    )
    parser.add_argument(
        '-r', '--remain', type=int, default=1, help='전기차 주차장 남은 공간'
    )
    parser.add_argument(
        '-w', '--wait', type=int, default=0, help='대기자'
    )
    return parser

reader = easyocr.Reader(['ko'], gpu=False) 

if not os.path.exists('result') :
    os.makedirs('result')

def main(args):
    cap = cv2.VideoCapture(0)
    
    width = int(cap.get(3)) # 가로 길이 가져오기 
    height = int(cap.get(4)) # 세로 길이 가져오기
    fps = 30
    cnt = 1

    fcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter('result/webcam.avi', fcc, fps, (width, height))

    charge = False
    db = SessionLocal()
    while (True) :
        k = cv2.waitKey(1) & 0xFF
        ret, frame = cap.read()
        if args.charge == 100:
            charge = False
        elif charge == True:
            args.charge += 1
        
        time.sleep(1)
        if ret:
            out.write(frame)
            cv2.imshow('frame', frame)
            result = reader.readtext(frame)
            print("detection....")
            answer =[]
            for i in range(len(result)):
                answer.append(result[i][1])
                print(answer)
            
            user = UserCreate
            for i in range(len(answer)):
                user = UserCreate
                user.car_number = answer[i]
                user = get_existing_user(db = db , user_create=user)
                if user:
                    cv2.imwrite('result/screenshot{}.png'.format(cnt), frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
                    
                    if user.elec_car == 0:
                        print('전기차가 아닙니다. 다른곳에 주차 바랍니다.')
                        break
                    
                    elif args.charge != 100:
                        text = '{}동 {}호 차량입니다. 전기차는 14시간동안 충전할수 있습니다.\n 현재 충전도는 {}% 입니다.'.format(user.building, user.unit, args.charge)
                        charge = True
                        print(text)
                        #speak(text)
                        break
                    
                    elif args.charge == 100 and args.remain == 0 and args.wait == 1:
                        text = '충전이 완료되었습니다. 현재 충전소의 대기자가 있습니다. 차를 빼주세요. '
                        print(text)
                        #speak(text)
                        break
                    
                    elif args.charge == 100:
                        text = '충전이 완료되었습니다. 차를 빼주세요.'
                        print(text)
                        #speak(text)
                        break
            cnt += 1
            if k == ord('q') :
                break
        else :
            print("Fail to read frame!")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    args = make_parser().parse_args()
    main(args)