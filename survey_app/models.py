from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	company_id = db.Column(db.String(12), unique=True, nullable=False)
	country_code = db.Column(db.String(8), nullable=False)
	email = db.Column(db.String(100))
	sections_completed = db.Column(db.Integer, default=0, nullable=False)

	def __repr__(self):
		return '<User %r>' % self.id


class ModelS1(db.Model):
	__tablename__ = 'section1'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	company_name = db.Column(db.String(40), nullable=False)
	economic_sector = db.Column(db.String(40), nullable=False)
	respondant_name = db.Column(db.String(40), nullable=False)
	respondant_position = db.Column(db.String(40), nullable=False)
	respondant_position_other = db.Column(db.String(40))
	phone = db.Column(db.String(12), nullable=False)
	country = db.Column(db.String(40), nullable=False)
	admin_div_1 = db.Column(db.String(40), nullable=False)
	admin_div_2 = db.Column(db.String(40), nullable=False)
	street = db.Column(db.String(80), nullable=False)
	street_number = db.Column(db.Integer, nullable=False)

	user = db.relationship('User', backref=db.backref('section1', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section1 %r>' % self.user_id


class ModelS2(db.Model):
	__tablename__ = 'section2'
	
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	local_products_entries = db.Column(db.Integer, nullable=False)
	exterior_products_entries = db.Column(db.Integer, nullable=False)
	exports_check = db.Column(db.Boolean)
	natural_people_participation = db.Column(db.Float, nullable=False)
	micro_businesses_participation = db.Column(db.Float, nullable=False)
	small_businesses_participation = db.Column(db.Float, nullable=False)
	medium_businesses_participation = db.Column(db.Float, nullable=False)
	big_businesses_participation = db.Column(db.Float, nullable=False)
	state_agencies_participation = db.Column(db.Float, nullable=False)
	natural_people_category = db.Column(db.String(80), nullable=False)
	micro_businesses_category = db.Column(db.String(80), nullable=False)
	small_businesses_category = db.Column(db.String(80), nullable=False)
	medium_businesses_category = db.Column(db.String(80), nullable=False)
	big_businesses_category = db.Column(db.String(80), nullable=False)
	state_agencies_category = db.Column(db.String(80), nullable=False)
	sales_volume = db.Column(db.Float, nullable=False)
	sales_volume_currency = db.Column(db.String(10), nullable=False)
	workers_number = db.Column(db.Integer, nullable=False)
	female_workers = db.Column(db.Integer, nullable=False)

	user = db.relationship('User', backref=db.backref('section2', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section2 %r>' % self.user_id


class ModelS2Products(db.Model):
	__tablename__ = 'section2_products'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	product_type = db.Column(db.String(10), nullable=False)
	product_country = db.Column(db.String(40))
	product_description = db.Column(db.String(40), nullable=False)
	product_quantity = db.Column(db.Float, nullable=False)
	product_unit = db.Column(db.String(40), nullable=False)

	user = db.relationship('User', backref=db.backref('section2_products', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section2 Products %r>' % self.user_id


class ModelS3(db.Model):
	__tablename__ = 'section3'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	production_area = db.Column(db.Float, nullable=False)
	production_area_unit = db.Column(db.String(40), nullable=False)
	production_turns = db.Column(db.Float, nullable=False)
	production_turn_hours = db.Column(db.Float, nullable=False)
	production_activity_monitoring = db.Column(db.String(80), nullable=False)
	jan_productive_cycle = db.Column(db.String(20), nullable=False)
	feb_productive_cycle = db.Column(db.String(20), nullable=False)
	mar_productive_cycle = db.Column(db.String(20), nullable=False)
	apr_productive_cycle = db.Column(db.String(20), nullable=False)
	may_productive_cycle = db.Column(db.String(20), nullable=False)
	jun_productive_cycle = db.Column(db.String(20), nullable=False)
	jul_productive_cycle = db.Column(db.String(20), nullable=False)
	aug_productive_cycle = db.Column(db.String(20), nullable=False)
	sep_productive_cycle = db.Column(db.String(20), nullable=False)
	oct_productive_cycle = db.Column(db.String(20), nullable=False)
	nov_productive_cycle = db.Column(db.String(20), nullable=False)
	dec_productive_cycle = db.Column(db.String(20), nullable=False)
	quality_complaints = db.Column(db.String(80), nullable=False)
	performance_complaints = db.Column(db.String(80), nullable=False)
	dispatch_complaints = db.Column(db.String(80), nullable=False)
	wrong_product_complaints = db.Column(db.String(80), nullable=False)
	web_page_usage = db.Column(db.String(80), nullable=False)
	facebook_usage = db.Column(db.String(80), nullable=False)
	twitter_usage = db.Column(db.String(80), nullable=False)
	linkedin_usage = db.Column(db.String(80), nullable=False)
	instagram_usage = db.Column(db.String(80), nullable=False)
	whatsapp_usage = db.Column(db.String(80), nullable=False)
	recent_investments = db.Column(db.String(80), nullable=False)
	recent_investments_amount = db.Column(db.Float)
	recent_investments_amount_currency = db.Column(db.String(10), nullable=False)

	user = db.relationship('User', backref=db.backref('section3', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section3 %r>' % self.user_id


class ModelS4(db.Model):
	__tablename__ = 'section4'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	manuals = db.Column(db.String(80), nullable=False)
	formal_meetings = db.Column(db.String(80), nullable=False)
	informal_meetings = db.Column(db.String(80), nullable=False)
	memos_letters = db.Column(db.String(80), nullable=False)
	intranet = db.Column(db.String(80), nullable=False)
	new_ideas_origin = db.Column(db.String(80), nullable=False)
	new_ideas_channel = db.Column(db.String(80), nullable=False)
	new_ideas_channel_other = db.Column(db.String(80))
	keep_staff_incentives = db.Column(db.String(80), nullable=False)
	productive_processes_investments = db.Column(db.String(80), nullable=False)
	recent_products_releases = db.Column(db.String(80), nullable=False)
	products_quality_changes = db.Column(db.String(80), nullable=False)
	associates = db.Column(db.String(80), nullable=False)
	associates_other = db.Column(db.String(80))
	dissemination_activities = db.Column(db.String(80), nullable=False)

	user = db.relationship('User', backref=db.backref('section4', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section4 %r>' % self.user_id


class ModelS5(db.Model):
	__tablename__ = 'section5'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	energy_sources = db.Column(db.String(80), nullable=False)
	energy_investments_financy = db.Column(db.String(80), nullable=False)
	energy_costs = db.Column(db.Float, nullable=False)
	energy_costs_currency = db.Column(db.String(10), nullable=False)
	water_consumption = db.Column(db.Float, nullable=False)
	water_consumption_unit = db.Column(db.String(40), nullable=False)
	water_costs = db.Column(db.Float, nullable=False)
	water_costs_currency = db.Column(db.String(10), nullable=False)
	waste_handling_1 = db.Column(db.String(80), nullable=False)
	waste_handling_2 = db.Column(db.String(80), nullable=False)
	waste_handling_3 = db.Column(db.String(80), nullable=False)
	waste_handling_4 = db.Column(db.String(80), nullable=False)
	waste_handling_5 = db.Column(db.String(80), nullable=False)

	user = db.relationship('User', backref=db.backref('section5', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section5 %r>' % self.user_id


class ModelS6(db.Model):
	__tablename__ = 'section6'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	operative_team = db.Column(db.String(40), nullable=False)
	administrative_team = db.Column(db.String(40), nullable=False)
	management_team = db.Column(db.String(40), nullable=False)
	training_programs = db.Column(db.String(80), nullable=False)

	user = db.relationship('User', backref=db.backref('section6', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section6 %r>' % self.user_id


class ModelS7(db.Model):
	__tablename__ = 'section7'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	surveillance_activities = db.Column(db.String(80), nullable=False)
	surveillance_activities_specification = db.Column(db.String(80))
	surveillance_activities_frequency = db.Column(db.String(80))
	third_party_licenses = db.Column(db.String(80), nullable=False)
	registered_licenses = db.Column(db.String(80), nullable=False)
	company_maintenance_type = db.Column(db.String(80), nullable=False)
	mechanical_maintenance = db.Column(db.String(80), nullable=False)
	electric_maintenance = db.Column(db.String(80), nullable=False)
	it_maintenance = db.Column(db.String(80), nullable=False)
	ot_maintenance = db.Column(db.String(80), nullable=False)

	user = db.relationship('User', backref=db.backref('section7', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Section7 %r>' % self.user_id


class ModelSp1(db.Model):
	__tablename__ = 'specific1'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


	user = db.relationship('User', backref=db.backref('specific1', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Specific1 %r>' % self.user_id


class ModelSp2(db.Model):
	__tablename__ = 'specific2'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


	user = db.relationship('User', backref=db.backref('specific2', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Specific2 %r>' % self.user_id


class ModelSp3(db.Model):
	__tablename__ = 'specific3'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


	user = db.relationship('User', backref=db.backref('specific3', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Specific3 %r>' % self.user_id


class ModelSp4(db.Model):
	__tablename__ = 'specific4'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


	user = db.relationship('User', backref=db.backref('specific4', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<Specific4 %r>' % self.user_id


class RecommendationsTable(db.Model):
	__tablename__ = 'recommendations_table'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	description = db.Column(db.String(160), nullable=False)
	condition = db.Column(db.String(160), nullable=False)

	def __repr__(self):
		return '<Recommendation %r>' % self.description


class UserRecommendations(db.Model):
	__tablename__ = 'user_recommendations'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
	recom_1 = db.Column(db.Boolean, nullable=False, default=False)
	recom_2 = db.Column(db.Boolean, nullable=False, default=False)
	recom_3 = db.Column(db.Boolean, nullable=False, default=False)
	recom_4 = db.Column(db.Boolean, nullable=False, default=False)
	recom_5 = db.Column(db.Boolean, nullable=False, default=False)
	recom_6 = db.Column(db.Boolean, nullable=False, default=False)
	recom_7 = db.Column(db.Boolean, nullable=False, default=False)
	recom_8 = db.Column(db.Boolean, nullable=False, default=False)
	recom_9 = db.Column(db.Boolean, nullable=False, default=False)


	user = db.relationship('User', backref=db.backref('user_recommendations', lazy=True, cascade="all, delete-orphan"))

	def __repr__(self):
		return '<User Recommendations %r>' % self.user_id