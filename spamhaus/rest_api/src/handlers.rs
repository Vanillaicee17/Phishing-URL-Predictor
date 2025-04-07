use actix_web::{web, HttpResponse};
use reqwest;

use crate::models::Item;

pub async fn get_data(domain_name: web::Path<String>) -> HttpResponse {
	let domain = domain_name.into_inner();
	let url = format!("https://www.spamhaus.org/api/v1/sia-proxy/api/intel/v2/byobject/domain/{}/overview", domain);

	let client = reqwest::Client::new();
	let response = client.get(&url)
		.header("User-Agent", "Actix-Web Client")
		.send()
		.await;

	match response {
		Ok(res) => {
			if res.status().is_success() {
				match res.json::<Item>().await {
					Ok(data) => HttpResponse::Ok().json(data),
					Err(e) => HttpResponse::InternalServerError().body(format!("Failed to deserialize JSON: {}", e))
					,
				}
			}
			else {
				HttpResponse::NotFound().body("Domain not found")
			}
		}
		Err(e) => HttpResponse::InternalServerError().body(format!("Failed to fetch data: {}", e)),
	}
}