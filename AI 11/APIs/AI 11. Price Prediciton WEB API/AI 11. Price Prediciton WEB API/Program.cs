var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

// Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var aiBasedUrl = builder.Configuration["AI_BASE"] ?? "http://localhost:8000";
builder.Services.AddHttpClient("ai",
    client =>
    {
        client.BaseAddress = new Uri(aiBasedUrl);
    }    
    );

builder.Services.AddCors(
    opt=>
    {
        opt.AddPolicy("ReactApp", policy =>
        {
            policy.WithOrigins("http://Localhost:5173")
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials();
        }); 
    }
    );

var app = builder.Build();

// Swagger UI
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
    app.MapOpenApi();
}

app.UseCors("ReactApp");
app.UseAuthorization();

app.MapControllers();

app.Run();
