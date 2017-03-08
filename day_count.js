cursor = db.antibiotic.aggregate(
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

while ( cursor.hasNext() ) {
   printjson( cursor.next() );
}