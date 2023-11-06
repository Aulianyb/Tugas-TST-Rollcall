# MICROSERVICE DEPLOYMENT : ROLL CALL
Nama : Aulia Nadhirah Yasmin Badrulkamal <br>
NIM : 18221066

## 🎲 Core Service
Core service yang diimplementasikan dalam microservice “Roll Call” adalah algoritma yang akan mencari user mana saja yang cocok dengan user yang saat ini sedang login berdasarkan minat boardgame kedua user tersebut, hasil dari algoritma ini juga diurutkan berdasarkan seberapa sama minat kedua user tersebut dengan user yang paling sama ada di urutan yang lebih tinggi. 

## ⚙ Teknologi yang digunakan
- FastAPI 0.104.1
- Pydantic 2.4.2
- Uvicorn 0.23.2

## 🌟 Fitur
- CRUD user
- CRUD board game
- CRUD city
- Login
- Logout
- Mendapatkan current user
- Matchmaking

## 👩‍💻 Cara Menjalankan
1. Gunakan link `http://tubes-tst-18221066-rollcall.azurewebsites.net/docs`
2. Menggunakan daftar API endpoint yang ada di situs tersebut, anda bisa menggunakan endpoint yang ada pada microservice ini dengan menekan opsi “try it out” pada setiap
3. API end point

## 📝 Algoritma Core Service
Tahapan yang dilakukan oleh algoritma matchmaking adalah :   
1. Mendapatkan currentUser, yaitu user yang sedang login pada saat ini
2. Apabila currentUser kosong, artinya belum ada user yang sudah login pada saat ini. Fungsi ini akan mengembalikan pesan “Tidak ada user yang logged in, harap logged in terlebih dahulu”
3. Fungsi akan melakukan iterasi pada daftar user dan melakukan checking apakah user memiliki atribut city yang sama dengan currentUser
4. Apabila user tersebut memiliki atribut city yang sama maka ia akan menjalankan fungsi how_many_similarities yang akan mengembalikkan jumlah board game yang sama dalam array boardgame currentUser dan user tersebut
5. Apabila jumlah boardgame yang sama lebih dari 0, maka fungsi ini akan menyimpan index dan jumlah board game yang sama dalam suatu array matchmaking 
6. Array matchmaking kemudian akan disorting berdasarkan seberapa sama minat kedua user tersebut dengan user yang paling sama ada di urutan yang lebih tinggi. 
7. Fungsi akan melakukan fetching dan mengambil data user berdasarkan index user yang ada dalam array matchmaking dan memasukkannya ke dalam array matchmaking_result, fungsi juga akan memasukkan berapa banyak kesamaan minat antara kedua user tersebut pada array matchmaking_result
8. Apabila array matchmaking kosong, maka fungsi akan mengembalikkan : “Maaf, sepertinya tidak ada player lain yang cocok denganmu :(”

## 🗺 API Endpoint
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/`
  - Mengembalikkan daftar seluruh user
- PUT `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/`
  - Melakukan update data user
- POST `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/`
  - Membuat user baru
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/{user_id}`
  - Mendapatkan data user dengan user_id yang dimasukkan
- DELETE `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/{user_id}`
  - Menghapus data user dengan user_id yang dimasukkan
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/find`
  - Mengembalikkan data user dengan username yang ada dalam query
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/city/`
  - Mengembalikkan daftar seluruh kota
- PUT `https://tubes-tst-18221066-rollcall.azurewebsites.net/city/`
  - Melakukan update data kota
- POST `https://tubes-tst-18221066-rollcall.azurewebsites.net/city/`
  - Membuat kota baru
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/city/{city_id}`
  - Mendapatkan data kota dengan city_id yang dimasukkan
- DELETE `https://tubes-tst-18221066-rollcall.azurewebsites.net/user/{city_id}`
  - Menghapus data kota dengan city_id yang dimasukkan
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/boardgame/`
  - Mengembalikkan daftar seluruh board game
- PUT `https://tubes-tst-18221066-rollcall.azurewebsites.net/boardgame/`
  - Melakukan update data board game
- POST `https://tubes-tst-18221066-rollcall.azurewebsites.net/boardgame/`
  - Membuat board game baru
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/boardgame/{boardgame_id}`
  - Mendapatkan data board game dengan boardgame_id yang dimasukkan
- DELETE `https://tubes-tst-18221066-rollcall.azurewebsites.net/boardgame/{boardgame_id}`
  - Menghapus data board game dengan boardgame_id yang dimasukkan
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/auth/currentUser`
  - Mengembalikkan data user yang sedang login pada saat ini
- POST `https://tubes-tst-18221066-rollcall.azurewebsites.net/auth/login`
  - Melakukan login user
- DELETE `https://tubes-tst-18221066-rollcall.azurewebsites.net/auth/logout`
  - Melakukan logout user
- GET `https://tubes-tst-18221066-rollcall.azurewebsites.net/matchmaking`
  - Mengembalikkan hasil matchmaking user yang saat ini sedang login
