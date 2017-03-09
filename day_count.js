
	cursor = collection.aggregate(
		[
			{
				$group:
				{
					_id :
					{
						day :
						{
							$cond : [
								{ $ifNull: ["$created_at", 0]},
								{ $dayOfMonth : "$created_at" },
								-2000
							]
						},
						month :
						{
							$cond :[
								{ $ifNull : ["$created_at", 0]},
								{ $month : "$created_at" },
								-2000
							]
						},
						year :
						{
							$cond : [
								{ $ifNull : ["$created_at", 0]},
								{ $year : "$created_at" },
								-2000
							]
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

	while ( cursor.hasNext() ) {
	   printjson( cursor.next() );
	}
