use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Item {
	pub domain: String,
	#[serde[rename = "last-seen"]]
	pub last_seen: i64,
	pub tags: Vec<String>,
	pub abused: bool,
	pub whois: Whois,
	pub score: i32,
	pub dimensions: Dimensions, 
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Whois{
	pub created:i64,
	pub expires: i64,
	pub registrar: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Dimensions {
    pub human: i32,
    pub identity: i32,
    pub infra: i32,
    pub malware: i32,
    pub smtp: i32,
}
