#!/bin/bash
read -s -p "Masukkan Kunci Enkripsi Database: " db_key
echo 
python3 src.py --key $db_key --env .env
