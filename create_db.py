from survey_app import create_app

app = create_app()

from survey_app.models import db, RecommendationsTable
from survey_app.recommendations import Recommendations


with app.app_context():
	db.create_all()

	# delete all recomendations in table
	for recommendation in RecommendationsTable.query.all():
		db.session.delete(recommendation)
	db.session.commit()

	# add recommendations
	for recommendation in Recommendations.recommendation_list:
		db.session.add(RecommendationsTable(description=recommendation[0], condition=recommendation[1]))
	db.session.commit()