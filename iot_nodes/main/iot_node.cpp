#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include "esp_log.h"
#include "mqtt_client.h"

#define BROKER_URI "mqtt://mqtt-broker"
static const char *TAG = "MQTT_NODE";

void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGI(TAG, "MQTT event received, event_id=%" PRIi32, event_id);

    switch (event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT client connected.");
            break;
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGI(TAG, "MQTT client disconnected.");
            break;
        case MQTT_EVENT_DATA:
            ESP_LOGI(TAG, "MQTT event data received.");
            break;
        default:
            ESP_LOGI(TAG, "Unhandled MQTT event.");
            break;
    }
}

extern "C" void app_main(void) {
    // Initialize the MQTT configuration
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker = {
            .address = {
                .uri = BROKER_URI,
            },
        },
    };

    // Initialize MQTT client
    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);

    // Register specific events for the MQTT client
    esp_mqtt_client_register_event(client, MQTT_EVENT_ANY, mqtt_event_handler, NULL);

    // Start the MQTT client
    esp_mqtt_client_start(client);
}
