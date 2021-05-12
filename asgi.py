from app import app 
import os

if __name__ == "__main__": 
    port1 = int(os.environ.get('PORT', 5000))
    # uvicorn.run(app, host='0.0.0.0', port=port1)
    app.run(host="0.0.0.0", port=port1)
    