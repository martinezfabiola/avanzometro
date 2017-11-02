from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .models import *


class TestRegister(TestCase):
    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def run_templateLogin(self):
        response=self.client.get('/login/')
        self.assertTemplateUsed(response, login.html)

    def test_login_details(self):
        # Issue a GET request.
        response = self.client.get('/login/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        
    def run_templates(self):
        response=self.client.get('/signup/')
        self.assertTemplateUsed(response, signup.html)

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/signup/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    # BASICAS:  Captura de los datos tipo post 

    def test_post_data(self):
        response = self.client.post('/signup/', 
            data = { 'username': 'laucv@gmail.com' , 'first_name': 'Lautaro','last_name': 'Villalon',
                 'password1': 'mipassword123',  'password2': 'mipassword123'
                })

        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(last_user.username, 'laucv@gmail.com')
        self.assertEquals(response.status_code, 302)


    #############################################################################
    #                           PRUEBAS DE FRONTERA                             #        
    #############################################################################

    # FRONTERA : Nombre no puede ser un campo vacio, el minimo que puede ser es 1 max 
    def test_name(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com' , 'first_name': 'l','last_name': 'Villalon',
                 'password1': 'mipassword123',  'password2': 'mipassword123'
                })

        self.assertEquals(User.objects.count(),1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.first_name), 1)


    # FRONTERA : Apellido no puede ser un campo vacio, el minimo que puede ser es 1
    def test_last_name(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com' , 'first_name': 'Lautaro','last_name':'v',
                 'password1': 'mipassword123',  'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(), 1)



    # FRONTERA : contraseña debe ser mayor a o igual a 8
    def test_password_length(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com' , 'first_name': 'Lautaro','last_name': 'Villalon',
                 'password1': 'pas21234',  'password2': 'pas21234'
                })
        self.assertEquals(User.objects.count(), 0)
      


    # FRONTERA : contraseña debe ser mayor a o igual a 8
    def test_password_length(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com' , 'first_name': 'Lautaro','last_name': 'Villalon',
                 'password1': 'pass1234',  'password2': 'pass1234'
                })
        self.assertEquals(User.objects.count(), 1)

        


    #############################################################################
    #                           PRUEBAS DE ESQUINA                              #        
    #############################################################################

    #ESQUINA:
    def test_min_name_max_last(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com', 'first_name': 'l','last_name': 'Villalon nosequemasp',
                'password1': 'mipassword123','password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.first_name), 1)
        self.assertEquals(len(last_user.last_name),20)


    #ESQUINA:
    def test_min_passowd_max_last(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com', 'first_name': 'Lautaro','last_name': 'Villalo nosequemaspu',
                'password1': 'mipassword123', 'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.last_name), 20)
        self.assertEquals(len(last_user.password1), 4)


    #############################################################################
    #                           PRUEBAS DE MALICIA                              #        
    #############################################################################

   #MALICIA: password menores al tamaño minimo 

    def test_min_passowd_max_last(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com','first_name': 'Lautaro','last_name': 'Villalon',
                 'password1': '', 'password2': ''
                })
        self.assertEquals(User.objects.count(), 0)


    #MALICIA: nombre con caracteres especiales
    def test_name_with_special_symbols(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv@gmail.com','first_name': 'Lautaro@#$@##','last_name': 'Villalon',
                 'password1': 'mipassword123', 'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(), 1)


    #MALICIA: email sin arroba. 
        
    def test_email(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv','first_name': 'Lautaro','last_name': 'Villalon',
                 'password1': 'mipassword123', 'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(),0 )

    #MALICIA: correo incompleto  contiene un solo punto 

    def test_email_imcomplete(self):
        response = self.client.post('/signup/', 
        data = { 'username': 'laucv.','first_name': 'Lautaro','last_name': 'Villalon',
                 'password1': 'mipassword123','password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(),0 )


    #MALICIA: contraseñas diferentes

    def test_diferents_password(self):
            response = self.client.post('/signup/', 
            data = { 'username': 'laucv@gmail.com','first_name': 'Lautaro','last_name': 'Villalon',
                     'password1': 'mipassword123','password2': 'mipassword456'
                    })
            self.assertEquals(User.objects.count(),0 )
