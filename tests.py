from django.test import TestCase
from django.contrib.auth.models import User



class TestRegister(TestCase):
    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()


   def test_details(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    # BASICAS:  Captura de los datos tipo post 

	def test_post_data(self):
		response = self.cliente.post('/signup', 
			data = { 'first_name': 'L','last_name': 'Villalon',
                'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })

		self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(last_user.username, 'laucv@gmail.com')
		self.assertEquals(response.status_code, 302)


    #############################################################################
    #                           PRUEBAS DE FRONTERA                             #        
    #############################################################################

    # FRONTERA : Nombre no puede ser un campo vacio, el minimo que puede ser es 1
    def test_name(self):
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'L','last_name': 'Villalon',
                'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })

        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.first_name), 1)


    # FRONTERA : Apellido no puede ser un campo vacio, el minimo que puede ser es 1
    def test_last_name(self):
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro','last_name': 'V',
                'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })

        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.last_mane), 1)


    # FRONTERA : contraseña debe ser mayor a o igual a 4
    def test_password_length(self):
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro','last_name': 'Villalon',
                'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })

        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.password1), 4)


    # FRONTERA : contraseña debe ser mayor a o igual a 4
    def test_password_length(self):
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro','last_name': 'Villalon',
                'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })

        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.password1), 4)


    #############################################################################
    #                           PRUEBAS DE ESQUINA                              #        
    #############################################################################

    #ESQUINA:
    def test_min_name_max_last(self):
            response = self.cliente.post('/signup', 
            data = { 'first_name': 'L','last_name': 'Villalon nosequemaspu',
                    'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                    'password2': 'mipassword123'
                    })
    	self.assertEquals(User.objects.count(), 1)
		last_user = User.objects.first()
		self.assertEquals(len(last_user.first_name), 1)
		self.assertEquals(len(last_user.last_name),20)


    #ESQUINA:
    def test_min_passowd_max_last(self):
                response = self.cliente.post('/signup', 
                data = { 'first_name': 'Lautaro','last_name': 'Villalo nosequemaspu',
                        'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                        'password2': 'mipassword123'
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
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro','last_name': 'Villalon',
                'username': 'laucv@gmail.com', 'password1': '',
                'password2': ''
                })
        self.assertEquals(User.objects.count(), 0)


    #MALICIA: nombre con caracteres especiales
     def test_name_with_special_symbols(self):
            response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro@#$@##','last_name': 'Villalon',
                'username': 'laucv@gmail.com', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(), 0)


    #MALICIA: email sin arroba. 
        
    def test_email(self):
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro','last_name': 'Villalon',
                'username': 'laucv', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(),0 )

    #MALICIA: correo incompleto  contiene un solo punto 

    def test_email_imcomplete(self):
        response = self.cliente.post('/signup', 
        data = { 'first_name': 'Lautaro','last_name': 'Villalon',
                'username': 'laucv.', 'password1': 'mipassword123',
                'password2': 'mipassword123'
                })
        self.assertEquals(User.objects.count(),0 )


    #MALICIA: contraseñas diferentes

    def test_diferents_password(self):
            response = self.cliente.post('/signup', 
            data = { 'first_name': 'Lautaro','last_name': 'Villalon',
                    'username': 'laucv.', 'password1': 'mipassword123',
                    'password2': 'mipassword456'
                    })
            self.assertEquals(User.objects.count(),0 )



    



