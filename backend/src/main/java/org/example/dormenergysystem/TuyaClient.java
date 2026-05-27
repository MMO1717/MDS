package org.example.dormenergysystem;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class TuyaClient {
    private final TuyaProperties properties;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final HttpClient httpClient = HttpClient.newHttpClient();

    private String accessToken;
    private long tokenExpireAtMillis;

    public TuyaClient(TuyaProperties properties) {
        this.properties = properties;
    }

    public JsonNode getStatus() throws Exception {
        String path = "/v2.0/cloud/thing/" + properties.getDeviceId() + "/shadow/properties";
        return send(HttpMethod.GET, path, "", true);
    }

    public JsonNode issueSwitch(boolean on) throws Exception {
        String path = "/v2.0/cloud/thing/" + properties.getDeviceId() + "/shadow/properties/issue";
        String switchJson = objectMapper.writeValueAsString(Map.of("switch_1", on));
        String body = objectMapper.writeValueAsString(Map.of("properties", switchJson));
        return send(HttpMethod.POST, path, body, true);
    }

    private JsonNode send(HttpMethod method, String path, String body, boolean withToken) throws Exception {
        validateConfig();
        String token = withToken ? getAccessToken() : "";
        String timestamp = String.valueOf(Instant.now().toEpochMilli());
        String nonce = UUID.randomUUID().toString();
        String sign = sign(method.name(), path, body, timestamp, nonce, token);

        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .uri(URI.create(properties.getBaseUrl() + path))
                .header("client_id", properties.getAccessId())
                .header("sign", sign)
                .header("t", timestamp)
                .header("sign_method", "HMAC-SHA256")
                .header("nonce", nonce);

        if (withToken) {
            builder.header("access_token", token);
        }

        if (method == HttpMethod.POST) {
            builder.header("Content-Type", MediaType.APPLICATION_JSON_VALUE)
                    .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8));
        } else {
            builder.GET();
        }

        HttpResponse<String> response = httpClient.send(builder.build(), HttpResponse.BodyHandlers.ofString());
        return objectMapper.readTree(response.body());
    }

    private String getAccessToken() throws Exception {
        long now = System.currentTimeMillis();
        if (accessToken != null && now < tokenExpireAtMillis - 60_000) {
            return accessToken;
        }

        String path = "/v1.0/token?grant_type=1";
        JsonNode json = send(HttpMethod.GET, path, "", false);
        if (!json.path("success").asBoolean(false)) {
            throw new IllegalStateException("获取 Tuya access_token 失败：" + json);
        }

        JsonNode result = json.path("result");
        accessToken = result.path("access_token").asText();
        tokenExpireAtMillis = now + result.path("expire_time").asLong(7200) * 1000;
        return accessToken;
    }

    private String sign(String method, String path, String body, String timestamp, String nonce, String token) throws Exception {
        String contentHash = sha256Hex(body == null ? "" : body);
        String stringToSign = method + "\n" + contentHash + "\n\n" + path;
        String signStr = properties.getAccessId() + token + timestamp + nonce + stringToSign;
        return hmacSha256(signStr, properties.getAccessSecret()).toUpperCase();
    }

    private String sha256Hex(String text) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(text.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(hash);
    }

    private String hmacSha256(String text, String secret) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        return bytesToHex(mac.doFinal(text.getBytes(StandardCharsets.UTF_8)));
    }

    private String bytesToHex(byte[] bytes) {
        StringBuilder builder = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            builder.append(String.format("%02x", b));
        }
        return builder.toString();
    }

    private void validateConfig() {
        if (isBlank(properties.getAccessId()) || isBlank(properties.getAccessSecret())) {
            throw new IllegalStateException("请先设置环境变量 TUYA_ACCESS_ID 和 TUYA_ACCESS_SECRET");
        }
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }
}
