from my_functions import *
from plate import *
from alerte import *
import cv2
import time
import re
import pandas as pd

def process_video(source):
    frame_size = (640, 480)
    save_video = True
    show_video = False
    save_img = True

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)
    cap = cv2.VideoCapture(source)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, frame_size)  # resizing image
            orifinal_frame = frame.copy()
            frame, results = object_detection(frame)

            rider_list = []
            head_list = []
            number_list = []

            for result in results:
                x1, y1, x2, y2, cnf, clas = result
                if clas == 0:
                    rider_list.append(result)
                elif clas == 1:
                    head_list.append(result)
                elif clas == 2:
                    number_list.append(result)

            for rdr in rider_list:
                time_stamp = str(time.time())
                x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                for hd in head_list:
                    x1h, y1h, x2h, y2h, cnfh, clash = hd
                    if inside_box([x1r, y1r, x2r, y2r], [x1h, y1h, x2h, y2h]):  # if head inside rider bbox
                        try:
                            head_img = orifinal_frame[y1h:y2h, x1h:x2h]
                            helmet_present = img_classify(head_img)
                        except:
                            helmet_present = [None, 0]

                        if helmet_present[0] == True:  # helmet present
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 0), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        elif helmet_present[0] == None:  # Poor prediction
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        elif helmet_present[0] == False:  # helmet absent
                            frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                            frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                            try:
                                cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                            except:
                                print('could not save rider')

                            for num in number_list:
                                x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                if inside_box([x1r, y1r, x2r, y2r], [x1_num, y1_num, x2_num, y2_num]):
                                    try:
                                        num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                        image_path = f'number_plates/{time_stamp}_{conf_num}.jpg'
                                        cv2.imwrite(image_path, num_img)
                                    except:
                                        print('could not save number plate')

            if save_video:  # save video
                out.write(frame)
            if save_img:  # save image
                cv2.imwrite('saved_frame.jpg', frame)
            if show_video:  # show video
                frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
                cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    process_number_plate_folder()
    print("\nRecognized License Plates:")
    pattern = r'^UK\d{2}[A-Z]{2}\d{4}$'
    print("\nValid UK Number Plates:")
    valid_plates = []

    for plate in recognized_plates:
        if re.match(pattern, plate):
            valid_plates.append(plate)
            print(plate)
    
    car_data=pd.read_excel("car_details.xlsx")
    for plate in valid_plates:
        match=car_data[car_data['Number_Plate']==plate]
        if not match.empty:
            owner_email = match.iloc[0]['Owner_Email']
            owner_name = match.iloc[0]['Owner_Name']
            subject = f"Traffic Violation Alert for {plate}"
            body = f"Dear {owner_name},\n\nYour vehicle with number plate {plate} has been detected violating traffic rules (no helmet).\n\nRegards,\nTraffic Monitoring System"
            email_alert(subject, body, owner_email)
        else:
            print(f"No record found for {plate}")

    # email_alert("Test Email", "This is a test email", "test@gmail.com")
    # if valid_plates:
    #     email_alert("Alert: Traffic Violation Detected", "Vehicle_detected.", "tester@gmail.com")

    print('Execution completed')


