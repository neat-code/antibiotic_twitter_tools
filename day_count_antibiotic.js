conn = new Mongo();
db = conn.getDB("antibiotic");

db.antibiotic.aggregate(
	[
		{ 
			$group: 
			{ 
				_id : 
				{ 
					day : 
					{ 
						$dayOfYear : "$created_at" 
					}, 
					year : { 
						$year : "$created_at" 
					} 
				}, 
				Count : 
				{ 
					$sum : 1 
				} 
			} 
		}
	]
)