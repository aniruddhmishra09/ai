from typing import Optional, Dict, Any


def weather_record_by_id(weather_alerts_response: Dict[str, Any], record_id: int) -> Optional[Dict[str, Any]]:
	"""
	Return a single weather record matching `record_id` from the
	`weather_alerts_response` returned by the application's loader.

	Args:
		weather_alerts_response: dict returned by `load_weather_data()` with keys
			like `status` and `data`.
		record_id: numeric id of the weather record to find.

	Returns:
		The matching record dict if found, otherwise None.
	"""
	
	if not weather_alerts_response or not weather_alerts_response.get("data"):
		return None

	data = weather_alerts_response.get("data", [])
	for rec in data:
		if rec is None:
			continue
		if str(rec.get("id")) == str(record_id):
			return rec

	return None

