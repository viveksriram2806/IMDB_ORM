from fastapi import FastAPI,Request

from ormsessionmaker import SessionMaker
from models import IMDB
from datetime import datetime

from datetime import datetime
import json

app=FastAPI()
session=SessionMaker().get_session()



def log_with_output(message, data):
    file_name = "output.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_str = json.dumps(data, ensure_ascii=False)

    line = f"[{timestamp}] {message} {data_str}"

    print(line)

    with open(file_name, "a") as f:
        f.write(line + "\n")


@app.put('/insert-data')
async def insert_data(request:Request):
    payload=await request.json()
    session_obj=session()
    for rec in payload:
        session_obj.add(IMDB(
            _id=rec['_id']['$oid'],
            popularity=rec.get('99popularity'),
            director=rec.get('director'),
            genre=str(rec.get('genre')),
            imdb_score=rec.get('imdb_score'),
            name=rec.get('name'),
            awards_won=rec.get('awards_won'),
            runtime_minutes=rec.get('runtime_minutes')


        ))
        session_obj.commit()
    session_obj.close()

    return {"message":"data inserted"}


@app.get('/get-data/{__id}')
def get_data(__id:int):
  session_obj=session()
  res=session_obj.query(IMDB).filter_by(imdb_id=__id).all()
  session_obj.close()
  response = {"detail": "Get data", "id": __id}
  log_with_output(f"{res},{__id}", response)
  return res

@app.post('/update-data/{_id}')
async def update_data(_id:int,request:Request):
    payload=await request.json()
    session_obj=session()
    res=session_obj.query(IMDB).filter_by(imdb_id=_id).first()
    
    res.director=payload['director']
    session_obj.commit()
    session_obj.close()
    response = {"detail": "Director updated", "id": _id}
    log_with_output(f"Director updated for ID {_id}", response)

    return {"data updated"}

@app.delete('/delete-data/{_id}')
def delete_data(_id:int):
    session_obj=session()
    res=session_obj.query(IMDB).filter_by(imdb_id=_id).first()

    session_obj.delete(res)
    session_obj.commit()
    session_obj.close()
    response = {"detail": "Data Deleted", "id": _id}
    log_with_output(f"Data Deleted for ID {_id}", response)

    
    return {"data deleted"}

if __name__=="__main__":
    app.run(debug=True)
