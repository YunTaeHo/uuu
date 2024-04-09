from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# 1. 데이터 베이스 모델 스키마 정의
class User(Base):
    __tablename__ = 'users' # 테이블 이름
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    
class Coin(Base):
    __tablename__ = 'coins' # 테이블 이름
    name = Column(String, primary_key=True)             
    drinkCan = Column(String) #result = 'cocacola' -- string
    dollarPrice = Column(String)
    realtimeBTC = Column(String)
    realtimeETH = Column(String)
    realtimeSOL = Column(String)
    realtimeXRP = Column(String)
    realtimeDOGE = Column(String)
    BTCforDollar = Column(String)
    ETHforDollar = Column(String)
    SOLforDollar = Column(String)
    XRPforDollar = Column(String)
    DOGEforDollar = Column(String)
    

# # 2. 데이터베이스 엔진 및 세션 생성
# DATABASE_URL = "sqlite:///./Test_fastapi_database.db"
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

COIN_URL = "sqlite:///./Coin.db"
engine = create_engine(
     COIN_URL, connect_args={"check_same_thread": False}
)

# 3. 데이터 베이스 테이블 생성
Base.metadata.create_all(bind=engine)


###### 이하 코드에서 연결해보기 ######
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
import os
import time
from binance.client import Client
import os



app = FastAPI()
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db # 요청 처리 동안 데이터베이스 세션
    finally:
        db.close() # 요청 처리가 끝나면 데이터베이스 세션을 닫기

# 1. 회원가입 구현
@app.post("/users")
def create_user(name: str, email: str, db: Session= Depends(get_db)):
    db_user = User(name=name, email=email)
    
    if db.query(User).filter(User.name == name).first():
        raise HTTPException(status_code=404, detail="User not found")
    
    db.add(db_user)
    db.commit()
    return {"name": db_user.name, "email" : email}

# 2. 전체 회원 조회 구현
@app.get("/users")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_dict = []
    
    for datas in users:
        user_dict.append({"id" : datas.id, "name": datas.name, "email":datas.email})
     
    return user_dict


#     name = Column(Integer, primary_key=True)             
#     drinkCan = Column(String), #result = 'cocacola' -- string
#     dollarPrice = Column(String)
#     realtimeBTC = Column(String)
#     realtimeETH = Column(String)
#     realtimeSOL = Column(String)
#     realtimeXRP = Column(String)
#     realtimeDOGE = Column(String)
#     BTCforDollar = Column(String)
#     ETHforDollar = Column(String)
#     SOLforDollar = Column(String)
#     XRPforDollar = Column(String)
#     DOGEforDollar = Column(String)

# 1. 회원가입 구현
@app.post("/coins")
def create_user(name: str, drinkCan: str, dollarPrice: str, realtimeBTC: str, realtimeETH: str,  realtimeSOL: str, realtimeXRP: str, realtimeDOGE: str,
                BTCforDollar: str, ETHforDollar: str, SOLforDollar: str, XRPforDollar: str, DOGEforDollar: str, db: Session= Depends(get_db)):
    
    db_coin = Coin(name=name, drinkCan=drinkCan, dollarPrice=dollarPrice, realtimeBTC=realtimeBTC, realtimeETH=realtimeETH,  realtimeSOL=realtimeSOL,
                   realtimeXRP=realtimeXRP, realtimeDOGE=realtimeDOGE, BTCforDollar=BTCforDollar,
                    ETHforDollar=ETHforDollar, SOLforDollar=SOLforDollar, XRPforDollar=XRPforDollar, DOGEforDollar=DOGEforDollar)
    
    
    if db.query(Coin).filter(Coin.name == name).first():
        raise HTTPException(status_code=404, detail="Coin does exist")
    
    db.add(db_coin)
    db.commit()
    return {"name" : db_coin.name, "drinkCan": db_coin.drinkCan, "dollarPrice":db_coin.dollarPrice,
                          "realtimeBTC" : db_coin.realtimeBTC, "realtimeETH": db_coin.realtimeETH, "realtimeSOL":db_coin.realtimeSOL,
                          "realtimeXRP" : db_coin.realtimeXRP, "realtimeDOGE": db_coin.realtimeDOGE, "BTCforDollar":db_coin.BTCforDollar,
                          "ETHforDollar" : db_coin.ETHforDollar, "SOLforDollar": db_coin.SOLforDollar, "XRPforDollar":db_coin.XRPforDollar,
                          "DOGEforDollar" : db_coin.DOGEforDollar}

# 2. 전체 회원 조회 구현
@app.get("/coins")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(Coin).all()
    user_dict = []
    
    for datas in users:
        user_dict.append({"name" : datas.name, "drinkCan": datas.drinkCan, "dollarPrice":datas.dollarPrice,
                          "realtimeBTC" : datas.realtimeBTC, "realtimeETH": datas.realtimeETH, "realtimeSOL":datas.realtimeSOL,
                          "realtimeXRP" : datas.realtimeXRP, "realtimeDOGE": datas.realtimeDOGE, "BTCforDollar":datas.BTCforDollar,
                          "ETHforDollar" : datas.ETHforDollar, "SOLforDollar": datas.SOLforDollar, "XRPforDollar":datas.XRPforDollar,
                          "DOGEforDollar" : datas.DOGEforDollar})
     
    return user_dict



# 3. 회원 데이터 수정
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = name
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return {"id": user_id, "name": name, "email": email}

# 4. 회원 데이터 삭제
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}



@app.put("/coins/Capture")
def create_user(db: Session= Depends(get_db)):
    
    # Initialize YOLO model
    model = YOLO(r'D:\Python\generative_AI_class_fastapi\crytpoSerach\runs\detect\train\weights\best.pt')

    # OpenCV camera capture
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

    detected_image_path = None
    detected_classes = ""
    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        
        # Perform object detection with YOLO
        results = model(frame)
        
        # Check if any objects were detected in any of the results
        objects_detected = False
        for result in results:
            # Assuming each 'result' in 'results' contains detected objects' information
            if len(result.boxes):  # Check if there are any detections
                objects_detected = True
                
                # Map class IDs to class names
                detected_classes = [result.names[int(cls)] for cls in result.boxes.cls.tolist()]
                print("Detected objects:", detected_classes)
                
                break

        if objects_detected:
            print("Objects detected. Stopping...")
            
            # Save the detected image
            save_path = "detected_image.jpg"
            results[0].save(save_path)  # Save the first detection result
            detected_image_path = save_path
            
            break
        
        # If the result is a list
        if isinstance(results, list):
            # If the result is a list, iterate over each detection result
            for result in results:
                # Save the detection result with bounding boxes
                save_path = "temp_detection.jpg"
                result.save(save_path)
                
                # Read the saved image using OpenCV
                im = cv2.imread(save_path)
                
                # Display the image with detected objects using matplotlib
                plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for display
                plt.axis('off')  # Do not show axis
                plt.show()
                
                # Remove the temporary image file
                os.remove(save_path)
                
        else:
            # If the result is not a list, it is a single detection result
            # Save the detection result with bounding boxes
            save_path = "temp_detection.jpg"
            results.save(save_path)
            
            # Read the saved image using OpenCV
            im = cv2.imread(save_path)
            
            # Display the image with detected objects using matplotlib
            plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for display
            plt.axis('off')  # Do not show axis
            plt.show()
            
            # Remove the temporary image file
            os.remove(save_path)
        
        # Pause for 2 seconds
        time.sleep(2)
        
        # Press 'q' to quit the loop and close the camera
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Display the detected image
    if detected_image_path:
        detected_im = cv2.imread(detected_image_path)
        plt.imshow(cv2.cvtColor(detected_im, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Detected Image")
        plt.show()

    ############################################################################
    reusltNum = 0

    korean_detected_classes = ''
    

    if detected_classes == ['cocacola']:
        reusltNum = 2
        
    elif  detected_classes == ['sprite']:
        reusltNum = 1.5
    elif  detected_classes == ['fanta']:
        reusltNum = 1

    print(detected_classes)
    print(reusltNum)
    # You can get an API key and secret by registering on the Binance website
    # It's recommended to use environment variables for security reasons
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')

    # Create the Binance client, providing the API key and secret
    client = Client(api_key, api_secret)

    # Function to get the latest price of a cryptocurrency
    def get_latest_price(symbol):
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    # Cryptocurrency to fetch price for
    crypto = 'BTCUSDT'

    # Fetch the latest price for Bitcoin
    btc_price = get_latest_price(crypto)

    # Print the current price of Bitcoin
    print(f"The current price of Bitcoin (BTC) is: ${btc_price}")

    # USD amount you want to spend on buying Bitcoin
    usd_to_spend = reusltNum  # You can change this value to any amount of USD you wish to spend

    # Calculate how much Bitcoin you can buy with the specified USD amount
    btc_to_buy = usd_to_spend / btc_price

    # Format the result to 8 decimal places
    btc_to_buy_formatted = "{:.8f}".format(btc_to_buy)

    # Print how much Bitcoin you can buy with the specified amount of USD, formatted to 8 decimal places
    print(f"With {usd_to_spend}$ = {btc_to_buy_formatted} BTC.")
            
   # db_coin = db.query(Coin).filter(Coin.name == detected_classes).first()######################################################################################
    detected_classes_str = ','.join(detected_classes)  # Convert list to comma-separated string

    db_coin = db.query(Coin).filter(Coin.name == detected_classes_str).first()
    #################################################################################################3
    if db_coin is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_coin.drinkCan = korean_detected_classes
    db_coin.dollarPrice = reusltNum
    
    # for crypto, price in crypto_prices.items():
    #     print(f"The current price of {crypto} is: ${price}")#realtime
        

    db_coin.realtimeBTC = btc_price
    # db_coin.realtimeETH = crypto_to_buy['ETHUSDT']
    # db_coin.realtimeSOL = crypto_to_buy['SOLUSDT']
    # db_coin.realtimeXRP = crypto_to_buy['XRPUSDT']
    # db_coin.realtimeDOGE = crypto_to_buy['DOGEUSDT']
    
    #db_coin.realtimeBTC = "a"
    db_coin.realtimeETH = "b"
    db_coin.realtimeSOL = "c"
    db_coin.realtimeXRP = "d"
    db_coin.realtimeDOGE = "e"
    
  #  db_coin.BTCforDollar = "A"
    db_coin.ETHforDollar = "B"
    db_coin.SOLforDollar = "C"
    db_coin.XRPforDollar = "D"
    db_coin.DOGEforDollar = "E"
    
    db_coin.BTCforDollar = btc_to_buy_formatted
    # db_coin.ETHforDollar = crypto_to_buy_formatted.items()[1]
    # db_coin.SOLforDollar = crypto_to_buy_formatted.items()[2]
    # db_coin.XRPforDollar = crypto_to_buy_formatted.items()[3]
    # db_coin.DOGEforDollar = crypto_to_buy_formatted.items()[4]
    
    db.commit()
    db.refresh(db_coin)
    
    #return {"name":"asdg"}
    return {"name" : db_coin.name, "drinkCan": db_coin.drinkCan, "dollarPrice":db_coin.dollarPrice,
                        "realtimeBTC" : db_coin.realtimeBTC, "realtimeETH": db_coin.realtimeETH, "realtimeSOL":db_coin.realtimeSOL,
                        "realtimeXRP" : db_coin.realtimeXRP, "realtimeDOGE": db_coin.realtimeDOGE, "BTCforDollar":db_coin.BTCforDollar,
                        "ETHforDollar" : db_coin.ETHforDollar, "SOLforDollar": db_coin.SOLforDollar, "XRPforDollar":db_coin.XRPforDollar,
                        "DOGEforDollar" : db_coin.DOGEforDollar}




# class Coin(Base):
#     __tablename__ = 'coins' # 테이블 이름
#     name = Column(Integer, primary_key=True)             
#     drinkCan = Column(String), #result = 'cocacola' -- string
#     dollarPrice = Column(String)
#     realtimeBTC = Column(String)
#     realtimeETH = Column(String)
#     realtimeSOL = Column(String)
#     realtimeXRP = Column(String)
#     realtimeDOGE = Column(String)
#     BTCforDollar = Column(String)
#     ETHforDollar = Column(String)
#     SOLforDollar = Column(String)
#     XRPforDollar = Column(String)
#     DOGEforDollar = Column(String)
    # name = 'dollarPrice', result = '2'       - Int
    # name = 'realtimeBTC', reuslt = '651843' - float
    # name = 'realtimeETH', reuslt = '35236'  -float
    # name = 'realtimeSOL', reuslt = '725'    -float
    # name = 'realtimeXRP', reuslt = '1.25'      -float
    # name = 'realtimeDOGE', reuslt = '0.05'  -float
    # name = 'BTCforDollar', result = '0.0000235'  -float
    # name = 'ETHforDollar', result = '0.0002635'  -float
    # name = 'SOLforDollar', result = '0.0326235'  -float
    # name = 'XRPforDollar', result = '1.2346235'  -float
    # name = 'DOGEforDollar', result = '9.2346345' -float