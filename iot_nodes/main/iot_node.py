#include <stdio.h>
#include <string>
#include <mqtt_client.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <esp_log.h>
#include <random>

#define BROKER_URI "mqtt://test.mosquitto.org" // Replace with your broker URI
#define TOPIC "iot/sensor_data"

static const char *TAG = "MQTT_EXAMPLE";

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGI(TAG, "MQTT event received, event_id=%d", event_id);

    esp_mqtt_event_handle_t event = (esp_mqtt_event_handle_t)event_data;
    esp_mqtt_client_handle_t client = event->client;

    switch (event->event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
            break;
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
            break;
        case MQTT_EVENT_PUBLISHED:
            ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_ERROR:
            ESP_LOGE(TAG, "MQTT_EVENT_ERROR");
            break;
        default:
            ESP_LOGI(TAG, "Unhandled MQTT event id=%d", event->event_id);
            break;
    }
}

void publish_temperature(esp_mqtt_client_handle_t client) {
    // Simulate a temperature sensor
    float temperature = 20.0 + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (15.0)));

    // Create JSON payload
    char payload[50];
    snprintf(payload, sizeof(payload), "{\"temperature\": %.2f}", temperature);

    // Publish to the MQTT topic
    int msg_id = esp_mqtt_client_publish(client, TOPIC, payload, 0, 1, 0);
    ESP_LOGI(TAG, "Published: %s (msg_id=%d)", payload, msg_id);
}

extern "C" void app_main() {
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = BROKER_URI,
    };

    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(client, MQTT_EVENT_ANY, mqtt_event_handler, NULL);

    ESP_LOGI(TAG, "Connecting to MQTT broker at %s", BROKER_URI);
    esp_mqtt_client_start(client);

    // Periodically publish temperature data
    while (true) {
        publish_temperature(client);
        vTaskDelay(pdMS_TO_TICKS(10000)); // Wait for 10 seconds
    }
}
