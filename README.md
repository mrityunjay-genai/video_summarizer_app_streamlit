# How to Deploy Streamlit app on EC2 instance

## 1. Login with your AWS console and launch an EC2 instance

## 2. Run the following commands

### Note: Do the port mapping to this port:- 8501

```bash
sudo apt update
```
```bash
sudo apt-get update
```
```bash
sudo apt upgrade -y
```

```bash
sudo apt install git curl unzip tar make sudo vim wget -y
```

```bash
sudo apt install python3-pip python3-venv -y
```

```bash
git clone "Your-repository"
```
```bash
cd <your_repo_folder>
```
```bash
nano .env <create and store env file and api key>
```
```bash
python3 -m  venv my_env
```
```bash
source my_env/bin/activate
```

```bash
pip3 install -r requirements.txt
```

```bash
#Temporary running
python3 -m streamlit run app.py
```

```bash
#Permanent running
nohup python3 -m streamlit run app.py
```

Note: Streamlit runs on this port: 8501



