from .models import db, User, ModelS1, ModelS2, ModelS2Products, ModelS3, ModelS4, ModelS5, ModelS6, ModelS7, ModelSp1, ModelSp2, ModelSp3, ModelSp4, UserRecommendations

class Recommendations:
	"""Clase usada para generar las recomendaciones para cada usuario.
	"""

	# lista de recomendaciones y descripción coloquial de cuando se gatilla
	recommendation_list = [
		('Debe informarse sobre la regulación sanitaria de los países de destino %s.', 'section1.economic_sector=="Alimentos y bebidas" and section2.exports_check==True'),
		('Debe implementar un sitio de ventas por internet con urgencia.','Si la suma de estos 3 % > 50%, y la pregunta de C102, al menos una de las plataformas no tiene la marcada la respuesta "Ventas online"'),
		('Se recomienda participar en las capacitaciones de Chilecompra.','state_agencies_participation > 30%'),
		('Se recomienda el establecimiento de un cuadro de control de tiempos y producción, entre otros.',''),
		('Se le recomienda diagnosticar el cuadro de indicadores operacionales, a través de un estudio (diagnóstico) que permita determinar indicadores clave del sistema, para redefinir tableros de gestión.',''),
		('Se le recomienda mantener actualizada la versión de su sistema, y que esta cuente con estándares de seguridad adecuados.','')
	]

	def __init__(self, user):
		"""
		Carga todas las tablas al inicializar un objeto de esta clase
		"""
		self.user = user
		self.s1 = ModelS1.query.filter_by(user=user).first()
		self.s2 = ModelS2.query.filter_by(user=user).first()
		self.s2_products = ModelS2Products.query.filter_by(user=user).all()
		self.s3 = ModelS3.query.filter_by(user=user).first()
		self.s4 = ModelS4.query.filter_by(user=user).first()
		self.s5 = ModelS5.query.filter_by(user=user).first()
		self.s6 = ModelS6.query.filter_by(user=user).first()
		self.s7 = ModelS7.query.filter_by(user=user).first()


	def recommendation1(self):
		"""
		Evalúa si se cumplen las condiciones para la recomendación 1

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""
		if self.s1.economic_sector == 'Alimentos y bebidas' and self.s2.exports_check:
			return True
		return False

	
	def recommendation2(self):
		"""
		Evalúa si se cumplen las condiciones para la recomendación 2

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""
		part1 = self.s2.natural_people_participation
		part2 = self.s2.micro_businesses_participation
		part3 = self.s2.small_businesses_participation
		web = self.s3.web_page_usage == 'Ventas online'
		facebook = self.s3.facebook_usage == 'Ventas online'
		twitter = self.s3.twitter_usage == 'Ventas online'
		linkedin = self.s3.linkedin_usage == 'Ventas online'
		instagram = self.s3.instagram_usage == 'Ventas online'
		whatsapp = self.s3.whatsapp_usage == 'Ventas online'
		if (part1 + part2 + part3) > 50 and not (web and facebook and twitter and linkedin and instagram and whatsapp):
			return True
		return False
	

	def recommendation3(self):
		"""
		Evalúa si se cumplen las condiciones para la recomendación 3

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""
		part = self.s2.state_agencies_participation
		if (part > 30):
			return True
		return False


	def recommendation4(self):
		"""
		Evalúa si se cumplen las condiciones para la recomendación 4

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""
		data = self.s3.production_activity_monitoring
		if (data == 'No se monitorea la productividad'):
			return True
		return False
	
	
	def recommendation5(self):
		"""
		Evalúa si se cumplen las condiciones para la recomendación 5

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""
		data = self.s3.production_activity_monitoring
		if (data == 'Mediante análisis básico de KPI: ventas, costos, utilidad' or data == 'Programa o sistema computacional genérico (planilla de cálculo o similares)'):
			return True
		return False


	def recommendation6(self):
		"""
		Evalúa si se cumplen las condiciones para la recomendación 6

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""
		data = self.s3.production_activity_monitoring
		if (data == 'Programa o sistema computacional especializado (ERP o similar)'):
			return True
		return False

	
	def get_recommendations(self):
		"""
		Evalúa todas las condiciones para un usuario y entrega una lista con las que cumple.

		Retorna:
			True
				si cumple las condiciones
			False
				si no
		"""

		# carga la lista de recomendaciones del usuario de la base de datos
		user_rec = UserRecommendations.query.filter_by(user=self.user).first()
		if user_rec:
			db.session.delete(user_rec)
			db.session.commit()

		# evalúa las condiciones
		recom_1=self.recommendation1()
		recom_2=self.recommendation2()
		recom_3=self.recommendation3()
		recom_4=self.recommendation4()
		recom_5=self.recommendation5()
		recom_6=self.recommendation6()

		# se agregan las recomendaciones a la base de datos
		query = UserRecommendations(user=self.user,
			recom_1=recom_1,
			recom_2=recom_2,
			recom_3=recom_3,
			recom_4=recom_4,
			recom_5=recom_5,
			recom_6=recom_6,
		)
		db.session.add(query)
		db.session.commit()

		# lista de recomendaciones que se va a retornar
		recommendations = []
		if recom_1:
			# query para encontrar la lista de países en los que exporta
			results = db.session.execute(
				f'''
				SELECT DISTINCT product_country FROM section2_products
				WHERE product_type = 'Exterior' AND user_id = {self.user.id}
				'''
			)
			country_list = [ result[0] for result in results ]

			if len(country_list) == 1:
				countries = country_list[0]
			else:
				countries = f'{", ".join(country_list[:-1])} y {country_list[-1]}'

			recommendations.append(self.recommendation_list[0][0] % countries)
		
		if recom_2:
			recommendations.append(self.recommendation_list[1][0])
		
		if recom_3:
			recommendations.append(self.recommendation_list[2][0])

		if recom_4:
			recommendations.append(self.recommendation_list[3][0])
		
		if recom_5:
			recommendations.append(self.recommendation_list[4][0])
		
		if recom_6:
			recommendations.append(self.recommendation_list[5][0])

		return recommendations