use actix_web::{web, App, HttpServer};
mod models;
mod handlers;


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(
                web::scope("/domain")

                .route("/{domain_name}/overview", web::get().to(handlers::get_data))


                )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}