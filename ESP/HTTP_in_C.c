#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

int main() {
    // Define variables
    CURL *curl;
    CURLcode res;
    const char *url = "http://localhost:5000/receive";
    struct curl_slist *headers = NULL;
    // char *data;
    char *name = "John";
    long unix_timestamp = 1618511705;
    char string[100];

    // Create JSON string
    snprintf(string, sizeof(string), "{ \"name\": \"%s\", \"timestamp\": %ld }", name, (long)(unix_timestamp));

    // Initialize CURL
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    if(curl) {
        // Set headers
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, "Accept: text/plain");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set URL and data
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, string);

        // Perform the request
        res = curl_easy_perform(curl);

        // Check for errors
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }

        // Clean up
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    // Clean up global state
    curl_global_cleanup();
    return 0;
}
