#!/usr/bin/env python
#-*- coding:iso-8859-1 -*-

import re, httplib, urllib, urllib2, base64, getpass
from lxml import etree
from getpass import getpass

'''Comandos'''
comandos = []
comandos.append({'name' : '--myhome', 'description' : 'se all twits.'})
comandos.append({'name' : '--p', 'description' : 'post new status (twit).'})
comandos.append({'name' : '--su', 'description' : 'search user.'})
comandos.append({'name' : '--sc', 'description' : 'set a config.'})
comandos.append({'name' : 'helpa', 'description' : 'list all comands.'})

class BlueBirdCrude:

    def __init__(self):
        pass
        self.flag_login = 0
        self.conecta = httplib.HTTPConnection("twitter.com",80)
        print "\n============ PASSARO AZUL TOSCO ============\n"
        print "====== Configure o aplicativo \n"
        self.__setconfig__()
        self.get_comands()
		
    ''' Pega o comando do usuario '''
    def get_comands(self,c=''):
        if(c==''):
            self.comand  = raw_input("Entre com algum comando, 'helpa' para listagem de comandos = > ")
            self.get_comands(self.comand)
        elif(c=='helpa'):
            print "----------------------------------------------"
            for comando in comandos:
                print comando['name'] + " ~ " + comando['description']
                print "----------------------------------------------"
            self.get_comands()                
        elif(c=='--su'):
            self.__getuser__()
        elif(c=='--sc'):
            self.__setconfig_()
        elif(c=='--myhome'):
            self.__myhome__()
        elif(c=='--p'):
            twitada = raw_input('Digite sua twitada! XD : \n')
            t = self.__senddata__('http://twitter.com/statuses/update.xml',{'status':twitada})
            if(t):
                print "Twittado com sucesso!"
                self.get_comands()
            else:
                print "Erro ao twittar! >/"
                self.get_comands()
        else:
            self.comand  = raw_input("Comando invalido entre com 'helpa' para listagem de comandos = > ")
            self.get_comands(self.comand)

    def __getuser__(self):
        self.user = raw_input('Nick do usuario => ')
        if(re.match('^([A-Za-z0-9\_]){4,15}$',self.user)):
            self.conecta.request("GET", "/users/show/"+self.user+".xml")
            self.response = self.conecta.getresponse()
            if(self.response.status == 200):
                print "\n++++ usuario => %s encontrado" % (self.user)
                self.__displaysu__()
                self.get_comands()
            else:
                print "\n++++ usuario => %s nÃ£o encontrado" % (self.user)
                self.get_comands()
        else:
            print "\n++++ usuario => %s invalido" % (self.user)
            self.get_comands()

    def __displaysu__(self):
        archive = open('now.xml','w+')
        archive.write(self.response.read())
        archive.close()
        self.data_user_xml = etree.parse('now.xml')
        print "\nID => %s"%(self.data_user_xml.getroot().find('id').text)
        print "Quantidade de seguidores => %s"%(self.data_user_xml.getroot().find('followers_count').text)
        print "Quantidade de amigos => %s"%(self.data_user_xml.getroot().find('friends_count').text)
        print "Quantidade de twits => %s"%(self.data_user_xml.getroot().find('statuses_count').text)        
        print "Ultima twittada => %s \n"%(self.data_user_xml.getroot().find('status').find('text').text)

    ''' Exibe sua home '''
    def __myhome__(self):
        data_response = self.__senddata__('http://api.twitter.com/1/statuses/home_timeline.xml?count=10')
        if(data_response):
            archive = open('twithome.xml','w+')        
            archive.write(data_response.read())
            archive.close()
            print "#######"
            for event, element in etree.iterparse('twithome.xml'):
                if (element.tag == 'text'):
                    print element.text
                if (element.tag == 'screen_name'):
                    print "by: " + element.text                
                    print "#######"
        else:
            print "Ocorreu um erro! servidor pode ter caido ;( ou vc digitou incorreto os dados, sete as configurações novamente."
        self.get_comands()
            

    '''Seta uma configuração usuario e senha'''
    def __setconfig__(self):
        self.login = raw_input('Digite o seu login! => ')
        if(re.match('^([A-Za-z0-9\_]){4,15}$',self.login)):
            self.passwd = getpass('Digite sua senha! => ')
            print "Configurado com sucesso!\n"
        else:
            print "Login invalido!\n"
            self.__setconfig__()
            
    '''Envia uma requisisão ao servidor'''
    def __senddata__(self,url=None,data=None):
        if(data is not None):
            data = urllib.urlencode(data)
        passauth = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passauth.add_password(None,url,self.login,self.passwd)
        opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passauth))
        opener.addheaders = [ ( 'User-agent', 'Mozilla/5.0' ) ]
        return opener.open(urllib2.Request(url,data))
        

BlueBirdCrude()
