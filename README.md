## File Storage

FileStorage is a web application for storing files, built with FastAPI (Python) for the API backend and ReactJS for the user interface. It uses MongoDB as the database and allows users to store files in different categories (folders). Users can create, rename, and delete their own custom categories, as well as upload, download, rename, and delete files. Additionally, users can move files to trash or favorites, and view their history of actions on the site. The project also features a sidebar that displays useful information and options for users.

---

### Running the project 

  ```
  git clone https://github.com/AlekseyAmp/FileStorage-FastAPI-React.git
  ```

- make STORAGE directory (Files and categories will be stored there)
  - cd server/src
  - create folder STORAGE 

- make .env file 
    - cd server/src 
    - create .env
    - copy this and paste it into the .env
    
    ```.env
    DATABASE_URL=mongodb://localhost:27017/file-storage
    DATABASE_NAME=file-storage
    ACCESS_TOKEN_EXPIRES_IN=15
    JWT_ALGORITHM=RS256

    CLIENT_ORIGIN=http://localhost:3000

    JWT_PRIVATE_KEY=LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlCT2dJQkFBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVmlQWlJyVFpjd3l4RVhVRGpNaFZuCi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUUpBYm5LaENOQ0dOSFZGaHJPQ0RCU0IKdmZ2ckRWUzVpZXAwd2h2SGlBUEdjeWV6bjd0U2RweUZ0NEU0QTNXT3VQOXhqenNjTFZyb1pzRmVMUWlqT1JhUwp3UUloQU84MWl2b21iVGhjRkltTFZPbU16Vk52TGxWTW02WE5iS3B4bGh4TlpUTmhBaUVBbWRISlpGM3haWFE0Cm15QnNCeEhLQ3JqOTF6bVFxU0E4bHUvT1ZNTDNSak1DSVFEbDJxOUdtN0lMbS85b0EyaCtXdnZabGxZUlJPR3oKT21lV2lEclR5MUxaUVFJZ2ZGYUlaUWxMU0tkWjJvdXF4MHdwOWVEejBEWklLVzVWaSt6czdMZHRDdUVDSUVGYwo3d21VZ3pPblpzbnU1clBsTDJjZldLTGhFbWwrUVFzOCtkMFBGdXlnCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0t
    JWT_PUBLIC_KEY=LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZ3d0RRWUpLb1pJaHZjTkFRRUJCUUFEU3dBd1NBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVgppUFpSclRaY3d5eEVYVURqTWhWbi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==
    REFRESH_TOKEN_EXPIRES_IN=15
    ACCESS_TOKEN_EXPIRES_IN=60
    ```

- python -m venv venv
- activate venv
  - on Windows ```
               venv/scripts/activate
               ```
  - on Linux ```
             venv/bin/activate
             ```
- pip install -r requirements.txt
- uvicorn main:app --reload

#### Open another terminal and run the NodeJS server

- cd client 
- npm install dotenv
- npm start

---

### The stack

- **Python** - FastAPI framework for API design
- **ReactJS** - for the user interface
- **MongoDB** - Database
- **Beanie** library to connect database and FastAPI
- **File storage** - the local folder "STORAGE" which must be in the server/src directory

---

### Project description

Files are stored in categories (folders), there are 4 default categories (documents, images, music, video)

#### Actions with categories:

- You can create your custom categories
- Custom categories can rename and delete (in the future - download)
- Default categories can not be created manually, when you upload a file if you are not at the address of the custom category and you upload a file from the main page or one of the default categories, the file will define itself a Default category and allocate to itself in onda of 4

#### Actions with files: 

- Upload, download, rename, delete files
- You can move file to trash, in trash you can bring file back, download, rename, delete permanently
- You can move file to favorites, in favorites you can move file back, download, rename

#### All your actions on the site will be saved in the history, you can see the history on the page "History"

- History saves information about 
- Registration and every login
- Creating, deleting, (in the future - downloading) categories
- Upload, download, delete, rename, move to favorites or trash, move from favorites or trash

**On** the right side of the page there will always be a sidebar that shows your profile (nickname and notifications), today's statistics (how many uploads, downloads, deleted files) and disk space used