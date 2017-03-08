collection.find().forEach(function(element){
		if (element.created_at !== null && isString(element.created_at)) {
				element.created_at = new Date(Date.parse(element.created_at.replace(/( +)/, ' UTC$1')));
				collection.save(element);
		}
})

function isString (obj) {
  return (Object.prototype.toString.call(obj) === '[object String]');
}
