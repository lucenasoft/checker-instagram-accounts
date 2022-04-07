from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from random import choice
import emoji
import os

#lembrando que sera necessario somente colocar o login e senha de uma conta do instagram, depois de logado a verificação começara a partir desta conta.
locale = os. getcwd()
print(emoji.emojize("Olá, CODER :red_heart:",variant="emoji_type"))
login_inst = str(input('Login: ')) #login conta do instagram
senha_inst = str(input('Senha: ')) #senha conta do instagram
navegador_opc = int(input('''Navegador Vísivel = 1
Navegador Oculto = 2: '''))
#FUNÇÃO PARA LER O ARQUIVO TXT CONTENDO USERNAMES DAS CONTAS!
usernames = open('userdate\\config\\usernames.txt','r')
lst = []
linhas = usernames.readlines()
for linha in linhas:
        lst.append(linha)
#''' USERAGETS '''
lst_user = []
with open('userdate\\config\\useragents.txt','r') as f:
        while f.readline().__len__()>0:
                lst_user.append(f.readline().strip('\n'))
lista = choice(lst_user).strip(' ')

#OPÇÕES DO NAVEGADOR!
print('Iniciando navegador')
if navegador_opc == 1:
    path = 'userdate\\driver'
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={lista}')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    manager = ChromeDriverManager(path=path)
    driver = webdriver.Chrome(service=Service(manager.install()),chrome_options=chrome_options)
    agent = driver.execute_script("return navigator.userAgent")
    print (agent)
if navegador_opc == 2:
    path = 'userdate\\driver'
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={lista}')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    manager = ChromeDriverManager(path=path)
    driver = webdriver.Chrome(service=Service(manager.install()),chrome_options=chrome_options)
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    agent = driver.execute_script("return navigator.userAgent")
    print (agent)
    
#''' INPUTS PARA LOGIN E SENHA ANTES DE ABRIR O NAVEGADOR, RECEBEM AS INFROMAÇÕES DIGITADAS PARA PROSEGUIR NO LOGIN. '''
#login_input = str(input('Login: '))
#pass_input = str(input('Password: '))
com_verificação = 0
sem_verificação = 0
#LOGANDO NA CONTA DO INSTAGRAM
driver.get('https://www.instagram.com/')
sleep(2)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(login_inst)
sleep(2)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(senha_inst)
sleep(2)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
sleep(5)
#REALIZANDO E VERIFICANDO AS FUNÇÕES 1º = LOGIN SUCESSO OU CONTA COM ALGUM TIPO DE VERIFICAÇÃO.
try:
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div[1]/div/div[2]/button/div')
    print('Não conseguimos acessar a conta.')
    sleep(2)
    driver.close()
except:
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/div[2]')
    print('Login Sucesso.')
    for x in range(len(lst)):
        driver.get(f'https://www.instagram.com/{lst[x]}/') #PESQUISANDO AS CONTAS DO ARQUIVO TXT PARA VERIFICAR
        sleep(5)
        try:
            driver.find_element_by_xpath('/html/body/div/div[1]/div/div/h2')
            print('Perfil em verificação\n')
            com_verificação +=1
            f = open('userdate\\contas\\verificar.txt', 'a')
            f.write(f'Usuário: {lst[x]}\n') #SALVA EM UM TXT AS CONTAS COM VERIFICAÇÃO, VERIFICAR.TXT
            f.close()
            sleep(2)
        except:
            infors = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul').text
            ifrors = infors.split()
            print(f'Usuário: {lst[x]}\nPublicações: {ifrors[0]}\nSeguidores: {ifrors[2]}\nSeguindo: {ifrors[4]}\n \n')  #PRINT FINAL, INFORMAÇÕES SOBRE AS CONTAS, SE ESTÁ OU NÃO EM VERIFICAÇÃO.
            sem_verificação += 1
            f = open('userdate\\contas\\contas.txt', 'a')
            f.write(f'Usuário: {lst[x]}\nPublicações: {ifrors[0]}\nSeguidores: {ifrors[2]}\nSeguindo: {ifrors[4]}\n \n') #SALVANDO O PRINT EM UM TXT, CONTAS.TXT
            f.close()
            sleep(2)
print(f'Sem verificação: {sem_verificação} Com verificação: {com_verificação} ') #QUANTIDADE DE CONTAS COM VERIFICAÇÃO OU NÃO.
driver.close()