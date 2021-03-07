from flask import session
from wtforms import Form, BooleanField, StringField, PasswordField, validators, FormField, SelectField, ValidationError, HiddenField, RadioField, FieldList, SelectMultipleField, IntegerField, DecimalField
from wtforms.fields.html5 import EmailField, TelField, DateField
from .models import db, User, ModelS1, ModelS2, ModelS3, ModelS4, ModelS5, ModelS6, ModelS7


class Unique(object):
	def __init__(self, model, field, message='Este campo debe ser único'):
		self.model = model
		self.field = field
		self.message = message

	def __call__(self, form, field):
		row = self.model.query.filter(self.field == field.data).first()
		if row:
			if 'user_id' in session:
				user = User.query.filter_by(id=session['user_id']).first()
				if row.id != user.id:
					raise ValidationError(self.message)
			else:
				raise ValidationError(self.message)


class SkipValidationIf(object):
	def __init__(self, selector, target, value):
		self.selector = selector
		self.target = target
		self.value = value

	def __call__(self, form, field):
		if form[self.selector].data != self.value:
			form[self.target].data = None
			form[self.target].errors = []
			raise validators.StopValidation()



class RegisterForm(Form):
	class Meta:
		locales = ['es_ES', 'es']

	email = EmailField('Correo Electrónico', [validators.InputRequired()])


class LoginForm(Form):
	class Meta:
		locales = ['es_ES', 'es']

	login_company_id = StringField('ID único de la empresa', [validators.Length(max=12), validators.InputRequired()])

	def validate_login_company_id(self, field):
		if not User.query.filter_by(company_id=field.data).first():
			raise ValidationError('No hay ninguna encuesta con esta ID.')


class FormS1(Form):
	class Meta:
		locales = ['es_ES', 'es']

	company_name = StringField('Nombre de la empresa', [validators.Length(max=40), validators.InputRequired()])
	company_id = StringField('ID único de la empresa', [validators.Length(max=12), validators.InputRequired(), Unique(User, User.company_id, 'Esta ID ya está registrada.')])
	economic_sector = SelectField('Sector industrial principal', choices=[
		('Seleccione una opción...'),
		('Alimentos y bebidas'), 
		('Maderera'), 
		('Metalmecánica / Metalúrgica'),
		('Plásticos y derivados'),
		('Química'),
		('Muebles, objetos e iluminación'),
		('Productos e insumos textiles')], validators = [validators.NoneOf(values=[u'Seleccione una opción...'], message='Selección inválida.')])
	respondant_name = StringField('Nombre de quien responde la encuesta', [validators.Length(max=40), validators.InputRequired()])
	respondant_position = SelectField('Cargo', choices=[
		('Seleccione una opción...'),
		('Gerente General / Dueño / Director'), 
		('Gerente / Director de Operaciones'), 
		('Gerente / Director Comercial'),
		('Gerente / Director de Administración y/o Finanzas'),
		('Otro')], validators = [validators.NoneOf(values=[u'Seleccione una opción...'], message='Selección inválida.')])
	respondant_position_other = StringField('Especifique el cargo', [SkipValidationIf('respondant_position', 'respondant_position_other', 'Otro'), validators.Length(max=40), validators.InputRequired()])
	phone = TelField('Teléfono', [validators.Length(max=12), validators.InputRequired()])
	country = StringField('País', [validators.Length(max=40), validators.InputRequired()])
	country_code = HiddenField()
	admin_div_1 = StringField('Región', [validators.Length(max=40), validators.InputRequired()])
	admin_div_2 = StringField('Comuna', [validators.Length(max=40), validators.InputRequired()])
	street = StringField('Calle', [validators.Length(max=80), validators.InputRequired()])
	street_number = IntegerField('Número', [validators.InputRequired()])


class FormS2(Form):
	class Meta:
		locales = ['es_ES', 'es']

	class ProductEntries(object):
		def __init__(self, message=None):
			if not message:
				message = u'Este campo es obligatorio.'
			self.message = message

		def __call__(self, form, field):
			n = int(field.name[-1])
			if 'local' in field.name:
				entries = int(form.local_products_entries.data)
				for i in range(entries, 7):
					if n == i:
						field.errors = []
						field.data = None
						raise validators.StopValidation()
			else:
				entries = int(form.exterior_products_entries.data)
				if form.exports_check.data == False:
					form.exterior_products_entries.data = 0
					field.errors = []
					field.data = None
					raise validators.StopValidation()
				else:
					for i in range(entries, 7):
						if n == i:
							field.errors = []
							field.data = None
							raise validators.StopValidation()
	

	class ParticipationSum(object):
		def __init__(self, message=None):
			if not message:
				message = u'Las participaciones deben sumar 100%.'
			self.message = message

		def __call__(self, form, field):
			p1 = form.natural_people_participation.data
			p2 = form.micro_businesses_participation.data
			p3 = form.small_businesses_participation.data
			p4 = form.medium_businesses_participation.data
			p5 = form.big_businesses_participation.data
			p6 = form.state_agencies_participation.data

			if p1 and p2 and p3 and p4 and p5 and p6:
				if (p1 + p2 + p3 + p4 + p5 + p6) != 100:
					form.participation_sum = True
					raise ValidationError(self.message)
				

	local_products_entries = HiddenField()
	local_product_description = FieldList(StringField('Descripción del producto', validators=[ProductEntries(), validators.Length(max=40), validators.InputRequired()]), min_entries=7, max_entries=7)
	local_product_quantity = FieldList(DecimalField('Cantidad o volumen', validators=[ProductEntries(), validators.NumberRange(min=0), validators.InputRequired()]), min_entries=7, max_entries=7)
	local_product_unit = FieldList(StringField('Unidad de medida', validators=[ProductEntries(), validators.Length(max=20), validators.InputRequired()]), min_entries=7, max_entries=7)

	exports_check = BooleanField('Marque si la empresa exporta algún producto')
	exterior_products_entries = HiddenField()
	exterior_product_country = FieldList(StringField('País', validators=[ProductEntries(), validators.Length(max=40), validators.InputRequired()]), min_entries=7, max_entries=7)
	exterior_product_description = FieldList(StringField('Descripción del producto', validators=[ProductEntries(), validators.Length(max=40), validators.InputRequired()]), min_entries=7, max_entries=7)
	exterior_product_quantity = FieldList(DecimalField('Cantidad o volumen', validators=[ProductEntries(), validators.NumberRange(min=0), validators.InputRequired()]), min_entries=7, max_entries=7)
	exterior_product_unit = FieldList(StringField('Unidad de medida', validators=[ProductEntries(), validators.Length(max=20), validators.InputRequired()]), min_entries=7, max_entries=7)

	natural_people_participation = DecimalField('Participación de personas naturales', [ParticipationSum(), validators.NumberRange(min=0,max=100), validators.InputRequired()])
	micro_businesses_participation = DecimalField('Participación de microempresas', [ParticipationSum(), validators.NumberRange(min=0,max=100), validators.InputRequired()])
	small_businesses_participation = DecimalField('Participación de pequeñas empresas', [ParticipationSum(), validators.NumberRange(min=0,max=100), validators.InputRequired()])
	medium_businesses_participation = DecimalField('Participación de medianas empresas', [ParticipationSum(), validators.NumberRange(min=0,max=100), validators.InputRequired()])
	big_businesses_participation = DecimalField('Participación de grandes empresas', [ParticipationSum(), validators.NumberRange(min=0,max=100), validators.InputRequired()])
	state_agencies_participation = DecimalField('Participación de organismos del estado', [ParticipationSum(), validators.NumberRange(min=0,max=100), validators.InputRequired()])
	natural_people_category = RadioField('Canales de venta de personas naturales', choices=[('Intermediario'),('Beneficiario final')])
	micro_businesses_category = RadioField('Canales de venta de microempresas', choices=[('Intermediario'),('Beneficiario final')])
	small_businesses_category = RadioField('Canales de venta de pequeñas empresas', choices=[('Intermediario'),('Beneficiario final')])
	medium_businesses_category = RadioField('Canales de venta de medianas empresas', choices=[('Intermediario'),('Beneficiario final')])
	big_businesses_category = RadioField('Canales de venta de grandes empresas', choices=[('Intermediario'),('Beneficiario final')])
	state_agencies_category = RadioField('Canales de venta de organismos del estado', choices=[('Intermediario'),('Beneficiario final')])
	sales_volume = DecimalField('Indique su volumen de ventas del último año contable', [validators.NumberRange(min=0), validators.InputRequired()])
	sales_volume_currency = HiddenField()
	workers_number = IntegerField('Indique el número de trabajadores', [validators.NumberRange(min=0), validators.InputRequired()])
	female_workers = IntegerField('Indique cuántos de éstos son mujeres', [validators.NumberRange(min=0), validators.InputRequired()])


class FormS3(Form):
	class Meta:
		locales = ['es_ES', 'es']
	
	production_area = DecimalField('Indique el área que tiene actualmente asignada a producción', [validators.NumberRange(min=0), validators.InputRequired()])
	production_area_unit = StringField('Unidad de medida', [validators.Length(max=40), validators.InputRequired()])
	production_turns = DecimalField('¿Cuántos turnos tiene la empresa para producir?', [validators.NumberRange(min=0), validators.InputRequired()])
	production_turn_hours = DecimalField('¿Cuántas horas por turno tiene?', [validators.NumberRange(min=0), validators.InputRequired()])
	production_activity_monitoring = SelectField('¿Cómo monitorea y/o controla la productividad?', choices=[
		('Seleccione una opción...'),
		('No se monitorea la productividad'), 
		('Mediante análisis básico de KPI: ventas, costos, utilidad'), 
		('Programa o sistema computacional genérico (planilla de cálculo o similares)'),
		('Programa o sistema computacional especializado (ERP o similar)')], validators = [validators.NoneOf(values=[u'Seleccione una opción...'], message='Selección inválida.')])
	jan_productive_cycle = RadioField('Ciclo productivo de enero', choices=[('Temporada alta'),('Temporada baja')])
	feb_productive_cycle = RadioField('Ciclo productivo de febrero', choices=[('Temporada alta'), ('Temporada baja')])
	mar_productive_cycle = RadioField('Ciclo productivo de marzo', choices=[('Temporada alta'), ('Temporada baja')])
	apr_productive_cycle = RadioField('Ciclo productivo de abril', choices=[('Temporada alta'), ('Temporada baja')])
	may_productive_cycle = RadioField('Ciclo productivo de mayo', choices=[('Temporada alta'), ('Temporada baja')])
	jun_productive_cycle = RadioField('Ciclo productivo de junio', choices=[('Temporada alta'), ('Temporada baja')])
	jul_productive_cycle = RadioField('Ciclo productivo de julio', choices=[('Temporada alta'), ('Temporada baja')])
	aug_productive_cycle = RadioField('Ciclo productivo de agosto', choices=[('Temporada alta'), ('Temporada baja')])
	sep_productive_cycle = RadioField('Ciclo productivo de septiembre', choices=[('Temporada alta'), ('Temporada baja')])
	oct_productive_cycle = RadioField('Ciclo productivo de octubre', choices=[('Temporada alta'), ('Temporada baja')])
	nov_productive_cycle = RadioField('Ciclo productivo de noviembre', choices=[('Temporada alta'), ('Temporada baja')])
	dec_productive_cycle = RadioField('Ciclo productivo de diciembre', choices=[('Temporada alta'), ('Temporada baja')])
	# jan_high_season = BooleanField('Enero')
	# feb_high_season = BooleanField('Febrero')
	# mar_high_season = BooleanField('Marzo')
	# apr_high_season = BooleanField('Abril')
	# may_high_season = BooleanField('Mayo')
	# jun_high_season = BooleanField('Junio')
	# jul_high_season = BooleanField('Julio')
	# aug_high_season = BooleanField('Agosto')
	# sep_high_season = BooleanField('Septiembre')
	# oct_high_season = BooleanField('Octubre')
	# nov_high_season = BooleanField('Noviembre')
	# dec_high_season = BooleanField('Diciembre')
	# jan_low_season = BooleanField('Enero')
	# feb_low_season = BooleanField('Febrero')
	# mar_low_season = BooleanField('Marzo')
	# apr_low_season = BooleanField('Abril')
	# may_low_season = BooleanField('Mayo')
	# jun_low_season = BooleanField('Junio')
	# jul_low_season = BooleanField('Julio')
	# aug_low_season = BooleanField('Agosto')
	# sep_low_season = BooleanField('Septiembre')
	# oct_low_season = BooleanField('Octubre')
	# nov_low_season = BooleanField('Noviembre')
	# dec_low_season = BooleanField('Diciembre')
	quality_complaints = RadioField('Calidad', choices=[('Diaria'),('Semanal'),('Mensual'),('Trimestral'),('Semestral'),('Anual')])
	performance_complaints = RadioField('Prestaciones del producto', choices=[('Diaria'),('Semanal'),('Mensual'),('Trimestral'),('Semestral'),('Anual')])
	dispatch_complaints = RadioField('Tiempo / Proceso de despacho', choices=[('Diaria'),('Semanal'),('Mensual'),('Trimestral'),('Semestral'),('Anual')])
	wrong_product_complaints = RadioField('Se recibe producto incorrecto', choices=[('Diaria'),('Semanal'),('Mensual'),('Trimestral'),('Semestral'),('Anual')])
	web_page_usage = RadioField('Página Web', choices=[('No usamos'),('Información básica (contacto, productos)'),('Catálogo online'),('Ventas online'),('Promoción y Márketing')])
	facebook_usage = RadioField('Facebook', choices=[('No usamos'),('Información básica (contacto, productos)'),('Catálogo online'),('Ventas online'),('Promoción y Márketing')])
	twitter_usage = RadioField('Twitter', choices=[('No usamos'),('Información básica (contacto, productos)'),('Catálogo online'),('Ventas online'),('Promoción y Márketing')])
	linkedin_usage = RadioField('Linkedin', choices=[('No usamos'),('Información básica (contacto, productos)'),('Catálogo online'),('Ventas online'),('Promoción y Márketing')])
	instagram_usage = RadioField('Instagram', choices=[('No usamos'),('Información básica (contacto, productos)'),('Catálogo online'),('Ventas online'),('Promoción y Márketing')])
	whatsapp_usage = RadioField('Whatsapp', choices=[('No usamos'),('Información básica (contacto, productos)'),('Catálogo online'),('Ventas online'),('Promoción y Márketing')])
	recent_investments = RadioField('¿En los últimos 2 años ha adaptado, mejorado, ordenado o expandido la infraestructura física de su empresa?', choices=[('Sí'),('No')])
	recent_investments_amount = DecimalField('¿Cuánto invirtió en estas acciones?', [SkipValidationIf('recent_investments', 'recent_investments_amount', 'Sí'), validators.NumberRange(min=0), validators.InputRequired()])
	recent_investments_amount_currency = HiddenField()


class FormS4(Form):
	class Meta:
		locales = ['es_ES', 'es']

	manuals = RadioField('¿Cuenta su empresa con documentos o manuales en que se informe al personal sobre las prácticas de la empresa?', choices=[('Si'),('No')])
	formal_meetings = RadioField('Reuniones formales', choices=[('Diaria'),('Semanal'),('Mensual'),('Anual'),('Según se requiera')])
	informal_meetings = RadioField('Reuniones informales', choices=[('Diaria'),('Semanal'),('Mensual'),('Anual'),('Según se requiera')])
	memos_letters = RadioField('Memos / Cartas', choices=[('Diaria'),('Semanal'),('Mensual'),('Anual'),('Según se requiera')])
	intranet = RadioField('Intranet', choices=[('Diaria'),('Semanal'),('Mensual'),('Anual'),('Según se requiera')])
	new_ideas_origin = RadioField('¿Las oportunidades de mejora o creación de nuevos productos o servicios, de dónde provienen generalmente?', choices=[
		('Equipo directivo y su equipo cercano'),
		('Equipo al que impacta directamente el desafío'),
		('Equipo transversal a la organización: todos contribuyen con experiencia y conocimiento'),
		('Equipos entre distintas disciplinas o áreas')])
	new_ideas_channel = RadioField('Normalmente, ¿cómo se canalizan las ideas en torno a mejoras, innovaciones o nuevos desarrollos en la empresa?', choices=[
		('Equipo directivo propone o define nuevas ideas o proyectos'),
		('Colaboradores sugieren ideas usando mecanismos internos como buzones de ideas, concursos, plataforma web u otros'),
		('Colaboradores sugieren mejoras libremente, dentro de sus áreas de manera informal'),
		('Otro')])
	new_ideas_channel_other = StringField('Especifique', [SkipValidationIf('new_ideas_channel', 'new_ideas_channel_other', 'Otro'), validators.Length(max=80), validators.InputRequired()])
	keep_staff_incentives = RadioField('¿Existen incentivos monetarios o no monetarios para retener al personal?', choices=[('Si'),('No')])
	productive_processes_investments = RadioField('¿En los últimos 12 meses, ha implementado mejoras en procesos productivos asociados a la oferta de la empresa?', choices=[('Si'),('No')])
	recent_products_releases = RadioField('¿En los últimos 12 meses, ha lanzado nuevos productos o servicios al mercado o desarrollado actividades conducentes a ello?', choices=[('Si'),('No')])
	products_quality_changes = RadioField('¿En los últimos 12 meses, considera que la calidad de los productos o servicios ha cambiado?', choices=[('Si'),('No')])
	associates = RadioField('¿Cuenta la empresa con vínculos, alianzas o socios que le permitan adoptar nueva tecnología o mejorar sus procesos?', choices=[
		('No'),
		('Universidades'),
		('Centros / Institutos de investigación'),
		('Empresas (incluyendo a proveedores y clientes)'),
		('Centros de desarrollo/apoyo a negocios'),
		('Entidades de gobierno'),
		('Otro')])
	associates_other = StringField('Especifique', [SkipValidationIf('associates', 'associates_other', 'Otro'), validators.Length(max=80), validators.InputRequired()])
	dissemination_activities = RadioField('¿Ha participado en seminarios, ferias u otras actividades de diseminación de conocimientos en los últimos 24 meses?', choices=[('Si'),('No')])


class FormS5(Form):
	class Meta:
		locales = ['es_ES', 'es']
	
	energy_sources = HiddenField([validators.Length(max=120), validators.InputRequired()])
	energy_investments_financy = RadioField('¿Cuenta con financiamiento (propio o externo) para inversión tecnológica?', choices=[('Si'),('No')])
	energy_costs = DecimalField('¿Cuál es el costo anual que paga en energía?', [validators.NumberRange(min=0), validators.InputRequired()])
	energy_costs_currency = HiddenField()
	water_consumption = DecimalField('¿Qué volumen de agua consume anualmente?', [validators.NumberRange(min=0), validators.InputRequired()])
	water_consumption_unit = StringField('Unidad de medida', [validators.Length(max=40), validators.InputRequired()])
	water_costs = DecimalField('¿Cuál es el costo anual que paga por agua?', [validators.NumberRange(min=0), validators.InputRequired()])
	water_costs_currency = HiddenField()
	waste_handling_1 = RadioField('Líquidos no peligrosos (lavado, limpieza y detergentes)', choices=[
		('Nada'),
		('Nada, aunque tiene potencial'),
		('Se reutiliza en la misma empresa'),
		('Se vende a terceros'),
		('Se recicla por terceros'),
		('Se incinera'),
		('Se usa para compostaje o alimentación')
	])
	waste_handling_2 = RadioField('Líquidos peligrosos (inflamables, corrosivos, reactivos, tóxicos, explosivos, infecciosos, radioactivos)', choices=[
		('Nada'),
		('Nada, aunque tiene potencial'),
		('Se reutiliza en la misma empresa'),
		('Se vende a terceros'),
		('Se recicla por terceros'),
		('Se incinera'),
		('Se usa para compostaje o alimentación')
	])
	waste_handling_3 = RadioField('Orgánicos (desperdicios biodegradables)', choices=[
		('Nada'),
		('Nada, aunque tiene potencial'),
		('Se reutiliza en la misma empresa'),
		('Se vende a terceros'),
		('Se recicla por terceros'),
		('Se incinera'),
		('Se usa para compostaje o alimentación')
	])
	waste_handling_4 = RadioField('Sólidos no reciclables', choices=[
		('Nada'),
		('Nada, aunque tiene potencial'),
		('Se reutiliza en la misma empresa'),
		('Se vende a terceros'),
		('Se recicla por terceros'),
		('Se incinera'),
		('Se usa para compostaje o alimentación')
	])
	waste_handling_5 = RadioField('Sólidos reciclables (plásticos, vidrio, metal, papel/cartón)', choices=[
		('Nada'),
		('Nada, aunque tiene potencial'),
		('Se reutiliza en la misma empresa'),
		('Se vende a terceros'),
		('Se recicla por terceros'),
		('Se incinera'),
		('Se usa para compostaje o alimentación')
	])


class FormS6(Form):
	class Meta:
		locales = ['es_ES', 'es']
	
	operative_team = RadioField('Equipo Operativo', choices=[
		('Escuela / Liceo incompleto'),
		('Escuela / Liceo completo'),
		('Técnico-profesional incompleto'),
		('Técnico-profesional completo'),
		('Universitaria incompleta'),
		('Universitaria completa'),
		('Postgrado incompleto'),
		('Postgrado completo')
		])
	administrative_team = RadioField('Equipo Administrativo', choices=[
		('Escuela / Liceo incompleto'),
		('Escuela / Liceo completo'),
		('Técnico-profesional incompleto'),
		('Técnico-profesional completo'),
		('Universitaria incompleta'),
		('Universitaria completa'),
		('Postgrado incompleto'),
		('Postgrado completo')
		])
	management_team = RadioField('Equipo Gerencial', choices=[
		('Escuela / Liceo incompleto'),
		('Escuela / Liceo completo'),
		('Técnico-profesional incompleto'),
		('Técnico-profesional completo'),
		('Universitaria incompleta'),
		('Universitaria completa'),
		('Postgrado incompleto'),
		('Postgrado completo')
		])
	
	training_programs = RadioField('¿Ha ejecutado programas de formación/entrenamiento en los últimos 2 años?', choices=[
		('No'),
		('Inducción'),
		('Actualización de conocimientos'),
		('Capacitación técnica'),
		('En el puesto de trabajo'),
		('Habilidades blandas'),
		('Habilidades directivas')])


class FormS7(Form):
	class Meta:
		locales = ['es_ES', 'es']

	surveillance_activities = RadioField('¿Lleva a cabo la empresa actividades de vigilancia tecnológica?', choices=[('Sí'),('No')])
	surveillance_activities_specification = RadioField('¿Cómo las lleva a cabo?', choices=[
		('Leyendo revistas técnicas'),
		('Informes personalizados'),
		('Servicios de suscripción'),
		('Reuniones con expertos'),
		('Visitas a ferias'),
		('Escaneo o revisión de patentes'),
		('Software open source')], validators=[SkipValidationIf('surveillance_activities', 'surveillance_activities_specification', 'Sí')])
	surveillance_activities_frequency = RadioField('¿Qué tan frecuentemente lo hace?', choices=[
		('Mensual'),
		('Trimestral'),
		('Anual'),
		('Otro')], validators=[SkipValidationIf('surveillance_activities', 'surveillance_activities_frequency', 'Sí')])
	third_party_licenses = RadioField('¿Usa la empresa licencias de terceros? (hardware o software)', choices=[('Si'),('No')])
	registered_licenses = RadioField('¿Ha registrado la empresa algún tipo de Propiedad Intelectual / Industrial?', choices=[
		('No'),
		('Registro de marca'),
		('Secreto industrial'),
		('Patentes'),
		('Derechos de autor'),
		('Diseños industriales'),
		('Indicación geográfica'),
		('Diseño de circuitos impresos'),
		('Variedades vegetales')])
	company_maintenance_type = RadioField('El mantenimiento en la empresa es de tipo', choices=[
		('Reactivo'),
		('Preventivo'),
		('Predictivo')])
	mechanical_maintenance = RadioField('Mecánico', choices=[
		('No'),
		('Sí, no formal'),
		('Sí, impreso')])
	electric_maintenance = RadioField('Eléctrico', choices=[
		('No'),
		('Sí, no formal'),
		('Sí, impreso')])
	it_maintenance = RadioField('Tecnologías de información', choices=[
		('No'),
		('Sí, no formal'),
		('Sí, impreso')])
	ot_maintenance = RadioField('Tecnologías de operación', choices=[
		('No'),
		('Sí, no formal'),
		('Sí, impreso')])


class FormSp1(Form):
	class Meta:
		locales = ['es_ES', 'es']

	class AnyOfMulti(object):
		field_flags = ('one_required', )

		def __init__(self, selectors, message=None):
			self.selectors = selectors
			if not message:
				message = u'Seleccione al menos una opción.'
			self.message = message

		def __call__(self, form, field):
			checks = False
			for selector in self.selectors:
				if form[selector].data:
					checks = True
			if not checks:
				raise ValidationError()
	

	software_for_sales = BooleanField('Sí, para la venta de productos', validators=[AnyOfMulti(['software_for_sales', 'software_for_production', 'not_software_but_needed', 'not_software_needed'])])
	software_for_sales_name = StringField('Nombre del software', [SkipValidationIf('software_for_sales', 'software_for_sales_name', True), validators.Length(max=40), validators.InputRequired()])
	software_for_sales_rate = RadioField('¿Cómo lo considera?', choices=[('Muy bueno'),('Bueno'),('Regular'),('Malo')], validators=[SkipValidationIf('software_for_sales', 'software_for_sales_rate', True)])
	software_for_sales_adquisition = RadioField('¿Cómo lo adquirió?', choices=[('Licencia temporal'),('Compra única'),('Diseñado a la medida'),('Gratuito')], validators=[SkipValidationIf('software_for_sales', 'software_for_sales_adquisition', True)])

	software_for_production = BooleanField('Sí, asociado a la producción', validators=[AnyOfMulti(['software_for_sales', 'software_for_production', 'not_software_but_needed', 'not_software_needed'])])
	software_for_production_name = StringField('Nombre del software', [SkipValidationIf('software_for_production', 'software_for_production_name', True), validators.Length(max=40), validators.InputRequired()])
	software_for_production_rate = RadioField('¿Cómo lo considera?', choices=[('Muy bueno'),('Bueno'),('Regular'),('Malo')], validators=[SkipValidationIf('software_for_production', 'software_for_production_rate', True)])
	software_for_production_adquisition = RadioField('¿Cómo lo adquirió?', choices=[('Licencia temporal'),('Compra única'),('Diseñado a la medida'),('Gratuito')], validators=[SkipValidationIf('software_for_production', 'software_for_production_adquisition', True)])

	not_software_but_needed = BooleanField('No, pero consideramos que es una necesidad para la empresa', validators=[AnyOfMulti(['software_for_sales', 'software_for_production', 'not_software_but_needed', 'not_software_needed'])])
	not_software_needed = BooleanField('No, por ahora no lo necesitamos', validators=[AnyOfMulti(['software_for_sales', 'software_for_production', 'not_software_but_needed', 'not_software_needed'])])

	automation_level =  RadioField('Especifique el nivel de automatización de su empresa', choices=[
		('Manual'),
		('Semiautomatizado'),
		('Automatizado')])
	no_cert = BooleanField('No', validators=[AnyOfMulti(['no_cert', 'authority_cert', 'gmp_cert', 'haccp_cert', 'fssc22000_cert', 'global_gap_cert'])])
	authority_cert = BooleanField('Resolución o certificado sanitario de la autoridad', validators=[AnyOfMulti(['no_cert', 'authority_cert', 'gmp_cert', 'haccp_cert', 'fssc22000_cert', 'global_gap_cert'])])
	authority_cert_start_date = DateField('Fecha de inicio vigencia', validators=[SkipValidationIf('authority_cert', 'authority_cert_start_date', True)])
	authority_cert_end_date = DateField('Fecha de término vigencia', validators=[SkipValidationIf('authority_cert', 'authority_cert_end_date', True)])
	gmp_cert = BooleanField('GMP', validators=[AnyOfMulti(['no_cert', 'authority_cert', 'gmp_cert', 'haccp_cert', 'fssc22000_cert', 'global_gap_cert'])])
	gmp_cert_start_date = DateField('Fecha de inicio vigencia', validators=[SkipValidationIf('gmp_cert', 'gmp_cert_start_date', True)])
	gmp_cert_end_date = DateField('Fecha de término vigencia', validators=[SkipValidationIf('gmp_cert', 'gmp_cert_end_date', True)])
	haccp_cert = BooleanField('HACCP', validators=[AnyOfMulti(['no_cert', 'authority_cert', 'gmp_cert', 'haccp_cert', 'fssc22000_cert', 'global_gap_cert'])])
	haccp_cert_start_date = DateField('Fecha de inicio vigencia', validators=[SkipValidationIf('haccp_cert', 'haccp_cert_start_date', True)])
	haccp_cert_end_date = DateField('Fecha de término vigencia', validators=[SkipValidationIf('haccp_cert', 'haccp_cert_end_date', True)])
	fssc22000_cert = BooleanField('FSSC22000', validators=[AnyOfMulti(['no_cert', 'authority_cert', 'gmp_cert', 'haccp_cert', 'fssc22000_cert', 'global_gap_cert'])])
	fssc22000_cert_start_date = DateField('Fecha de inicio vigencia', validators=[SkipValidationIf('fssc22000_cert', 'fssc22000_cert_start_date', True)])
	fssc22000_cert_end_date = DateField('Fecha de término vigencia', validators=[SkipValidationIf('fssc22000_cert', 'fssc22000_cert_end_date', True)])
	global_gap_cert = BooleanField('GLOBAL GAP', validators=[AnyOfMulti(['no_cert', 'authority_cert', 'gmp_cert', 'haccp_cert', 'fssc22000_cert', 'global_gap_cert'])])
	global_gap_cert_start_date = DateField('Fecha de inicio vigencia', validators=[SkipValidationIf('global_gap_cert', 'global_gap_cert_start_date', True)])
	global_gap_cert_end_date = DateField('Fecha de término vigencia', validators=[SkipValidationIf('global_gap_cert', 'global_gap_cert_end_date', True)])


class FormSp2(Form):
	class Meta:
		locales = ['es_ES', 'es']

	smaller_diameter = DecimalField('Diámetro menor', [validators.NumberRange(min=0), validators.InputRequired()])
	bigger_diameter = DecimalField('Diámetro mayor', [validators.NumberRange(min=0), validators.InputRequired()])

	a_control_volumen_entrada = BooleanField('Control de volumen de entrada')
	a_escaner_sombra = BooleanField('Escáner sombra (Determinación diámetro)')
	a_segregacion_por_calidad = BooleanField('Segregación por calidad')
	a_acopio_por_diametros = BooleanField('Acopio por diámetros')
	a_control_stock_diario = BooleanField('Control stock diario')
	a_maximo_dias_en_acopio = IntegerField('Número de días máximo en acopio', [validators.NumberRange(min=0), validators.InputRequired()])
	
	b_escaner_orientacion_trozo = BooleanField('Escáner orientación trozo')
	b_reductores_de_contrafuertes = BooleanField('Reductores de contrafuertes')
	b_escaner_optimizacion_rend = BooleanField('Escáner optimización (Rend)')
	b_posicionador_transversal = BooleanField('Posicionador transversal')
	b_reductores_laterales = BooleanField('Reductores laterales')
	b_mp_huincha_doble = BooleanField('MP huincha doble')
	b_mp_huincha_cuadruple = BooleanField('MP huincha cuádruple')
	b_mp_carro_huincha = BooleanField('MP carro huincha')
	b_mp_s_circulares = BooleanField('MP S. circulares')
	b_reductor_lampazo = BooleanField('Reductor lampazo')
	b_huincha_partidora_vertical = BooleanField('Huincha partidora vertical')
	b_huincha_partidora_horizontal = BooleanField('Huincha partidora horizontal')
	b_escaner_optimizacion_ct = BooleanField('Escáner optimización (CT)')
	b_canteadora = BooleanField('Canteadora')
	b_multiple = BooleanField('Múltiple')
	b_zona_clasificacion_manual = BooleanField('Zona clasificación (manual)')
	b_zona_clasificacion_ia = BooleanField('Zona clasificación (IA)')
	b_segregacion_l_sl_c = BooleanField('Segregación L-SL-C')
	b_control_dimensiona_y_grado = BooleanField('Control dimension y grado')
	b_dimensionado_de_largo = BooleanField('Dimensionado de largo')
	b_empalillado_automatico = BooleanField('Empalillado automático')
	b_empalillado_manual = BooleanField('Empalillado manual')
	b_etiquetado_por_producto = BooleanField('Etiquetado por producto')
	b_acopio_por_producto = BooleanField('Acopio por producto')

	c_vapor_externo = BooleanField('Vapor externo')
	c_caldera_bm = BooleanField('Caldera BM')
	c_caldera_gas = BooleanField('Caldera Gas')
	c_caldera_fosil = BooleanField('Caldera Fósil')
	c_caldera_pellet = BooleanField('Caldera Pellet')
	c_segregacion_carga_l_sl_c = BooleanField('Segregación carga L-SL-C')
	c_segregacion_carga_espesor = BooleanField('Segregación carga espesor')
	c_camara_frontal = BooleanField('Cámara frontal')
	c_camara_frontal_n = IntegerField('N°', [SkipValidationIf('c_camara_frontal', 'c_camara_frontal_n', True), validators.NumberRange(min=0), validators.InputRequired()])
	c_camara_frontal_vol = StringField('Vol.', [SkipValidationIf('c_camara_frontal', 'c_camara_frontal_vol', True), validators.Length(max=20), validators.InputRequired()])
	c_camara_tunel = BooleanField('Cámara túnel')
	c_camara_tunel_n = IntegerField('N°', [SkipValidationIf('c_camara_tunel', 'c_camara_tunel_n', True), validators.NumberRange(min=0), validators.InputRequired()])
	c_camara_tunel_vol = StringField('Vol.', [SkipValidationIf('c_camara_tunel', 'c_camara_tunel_vol', True), validators.Length(max=20), validators.InputRequired()])
	c_camara_doble_tunel = BooleanField('Cámara doble túnel')
	c_camara_doble_tunel_n = IntegerField('N°', [SkipValidationIf('c_camara_doble_tunel', 'c_camara_doble_tunel_n', True), validators.NumberRange(min=0), validators.InputRequired()])
	c_camara_doble_tunel_vol = StringField('Vol.', [SkipValidationIf('c_camara_doble_tunel', 'c_camara_doble_tunel_vol', True), validators.Length(max=20), validators.InputRequired()])
	c_programa_por_tipo_de_fibra = BooleanField('Programa por tipo de fibra')
	c_programa_por_espesor = BooleanField('Programa por espesor')
	c_utilizacion_de_contrapesos = BooleanField('Utilización de contrapesos')
	c_control_de_probetas_de_tensiones = BooleanField('Control de probetas de tensiones')
	c_control_de_ch = BooleanField('Control de CH%')

	c_maximo_dias_en_acopio = IntegerField('Número de días máximo en acopio', [validators.NumberRange(min=0), validators.InputRequired()])

class FormSp3(Form):
	class Meta:
		locales = ['es_ES', 'es']


class FormSp4(Form):
	class Meta:
		locales = ['es_ES', 'es']

