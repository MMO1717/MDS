package org.example.dormenergysystem;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/plug")
@CrossOrigin(origins = "*")
public class PlugController {
    private final TuyaClient tuyaClient;

    public PlugController(TuyaClient tuyaClient) {
        this.tuyaClient = tuyaClient;
    }

    @PostMapping("/on")
    public Map<String, Object> turnOn() throws Exception {
        JsonNode result = tuyaClient.issueSwitch(true);
        return Map.of("action", "on", "tuya", result);
    }

    @PostMapping("/off")
    public Map<String, Object> turnOff() throws Exception {
        JsonNode result = tuyaClient.issueSwitch(false);
        return Map.of("action", "off", "tuya", result);
    }

    @GetMapping("/status")
    public Map<String, Object> status() throws Exception {
        JsonNode result = tuyaClient.getStatus();
        return Map.of("tuya", result);
    }

    @GetMapping("/monitor")
    public Map<String, Object> monitor() throws Exception {
        JsonNode result = tuyaClient.getStatus();
        Map<String, JsonNode> propertyMap = toPropertyMap(result);

        boolean switchOn = propertyMap.getOrDefault("switch_1", emptyNode()).path("value").asBoolean(false);
        double power = readValue(propertyMap, "cur_power") / 10.0;
        double voltage = readValue(propertyMap, "cur_voltage") / 10.0;
        double current = readValue(propertyMap, "cur_current") / 1000.0;
        double energy = readValue(propertyMap, "add_ele") / 100.0;

        String riskLevel = "低";
        boolean abnormalStatus = false;
        String abnormalType = "";
        String suggestion = "当前用电正常，保持良好用电习惯。";

        if (!switchOn) {
            suggestion = "插座当前关闭，暂无实时负载。";
        } else if (power >= 1200) {
            riskLevel = "高";
            abnormalStatus = true;
            abnormalType = "高功率违规";
            suggestion = "检测到疑似大功率电器，请及时确认并停止使用。";
        } else if (power >= 800) {
            riskLevel = "中";
            abnormalStatus = true;
            abnormalType = "高功率用电";
            suggestion = "当前功率偏高，建议减少多个电器同时使用。";
        } else if (power > 0) {
            suggestion = "插座正在正常供电，可继续观察功率变化。";
        }

        Map<String, Object> monitor = new LinkedHashMap<>();
        monitor.put("dormId", "A101");
        monitor.put("switchOn", switchOn);
        monitor.put("power", round(power));
        monitor.put("voltage", round(voltage));
        monitor.put("current", round(current));
        monitor.put("energy", round(energy));
        monitor.put("occupied", true);
        monitor.put("temperature", null);
        monitor.put("abnormalStatus", abnormalStatus);
        monitor.put("abnormalType", abnormalType);
        monitor.put("riskLevel", riskLevel);
        monitor.put("suggestion", suggestion);

        return monitor;
    }

    private Map<String, JsonNode> toPropertyMap(JsonNode tuyaResult) {
        Map<String, JsonNode> propertyMap = new LinkedHashMap<>();
        JsonNode properties = tuyaResult.path("result").path("properties");
        if (properties.isArray()) {
            for (JsonNode property : properties) {
                propertyMap.put(property.path("code").asText(), property);
            }
        }
        return propertyMap;
    }

    private double readValue(Map<String, JsonNode> propertyMap, String code) {
        return propertyMap.getOrDefault(code, emptyNode()).path("value").asDouble(0);
    }

    private JsonNode emptyNode() {
        return com.fasterxml.jackson.databind.node.MissingNode.getInstance();
    }

    private double round(double value) {
        return Math.round(value * 10.0) / 10.0;
    }
}
