package org.example.dormenergysystem;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api/teacher")
@CrossOrigin(origins = "*")
public class TeacherController {
    private final TeacherDataStore dataStore;

    public TeacherController(TeacherDataStore dataStore) {
        this.dataStore = dataStore;
    }

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of("status", "ok", "message", "teacher backend is running");
    }

    @PostMapping("/reload")
    public Map<String, Object> reload() throws IOException {
        dataStore.reload();
        return Map.of("status", "ok", "message", "data reloaded");
    }

    @GetMapping("/overview")
    public Map<String, Object> overview() {
        return dataStore.overview();
    }

    @GetMapping("/dashboard")
    public Map<String, Object> dashboard(@RequestParam(defaultValue = "10") int limit) {
        return dataStore.dashboard(limit);
    }

    @GetMapping("/dorms")
    public Map<String, Object> dorms(
            @RequestParam(name = "dorm_id", required = false) String dormId,
            @RequestParam(required = false) Integer floor,
            @RequestParam(name = "risk_level", required = false) String riskLevel,
            @RequestParam(name = "abnormal_type", required = false) String abnormalType,
            @RequestParam(name = "start_time", required = false) String startTime,
            @RequestParam(name = "end_time", required = false) String endTime,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(name = "page_size", defaultValue = "20") int pageSize
    ) {
        TeacherQuery query = new TeacherQuery(dormId, floor, riskLevel, abnormalType, startTime, endTime);
        return dataStore.paginate(dataStore.dormRecords(query), page, pageSize);
    }

    @GetMapping("/dorms/{dormId}")
    public Map<String, Object> dormSummary(@PathVariable String dormId) {
        return dataStore.dormSummary(dormId);
    }

    @GetMapping("/abnormal")
    public Map<String, Object> abnormal(
            @RequestParam(name = "dorm_id", required = false) String dormId,
            @RequestParam(required = false) Integer floor,
            @RequestParam(name = "risk_level", required = false) String riskLevel,
            @RequestParam(name = "abnormal_type", required = false) String abnormalType,
            @RequestParam(name = "start_time", required = false) String startTime,
            @RequestParam(name = "end_time", required = false) String endTime,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(name = "page_size", defaultValue = "20") int pageSize
    ) {
        TeacherQuery query = new TeacherQuery(dormId, floor, riskLevel, abnormalType, startTime, endTime);
        return dataStore.paginate(dataStore.abnormalRecords(query), page, pageSize);
    }

    @GetMapping("/floor-load")
    public Map<String, Object> floorLoad(
            @RequestParam(name = "dorm_id", required = false) String dormId,
            @RequestParam(required = false) Integer floor,
            @RequestParam(name = "risk_level", required = false) String riskLevel,
            @RequestParam(name = "abnormal_type", required = false) String abnormalType,
            @RequestParam(name = "start_time", required = false) String startTime,
            @RequestParam(name = "end_time", required = false) String endTime,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(name = "page_size", defaultValue = "20") int pageSize
    ) {
        TeacherQuery query = new TeacherQuery(dormId, floor, riskLevel, abnormalType, startTime, endTime);
        return dataStore.paginate(dataStore.floorLoadRecords(query), page, pageSize);
    }

    @GetMapping("/floor-summary")
    public Map<String, Object> floorSummary() {
        return Map.of("data", dataStore.floorSummary());
    }

    @GetMapping("/predictions")
    public Map<String, Object> predictions(
            @RequestParam(name = "dorm_id", required = false) String dormId,
            @RequestParam(required = false) Integer floor,
            @RequestParam(name = "risk_level", required = false) String riskLevel,
            @RequestParam(name = "abnormal_type", required = false) String abnormalType,
            @RequestParam(name = "start_time", required = false) String startTime,
            @RequestParam(name = "end_time", required = false) String endTime,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(name = "page_size", defaultValue = "20") int pageSize
    ) {
        TeacherQuery query = new TeacherQuery(dormId, floor, riskLevel, abnormalType, startTime, endTime);
        return dataStore.paginate(dataStore.predictionRecords(query), page, pageSize);
    }

    @GetMapping("/suggestions")
    public Map<String, Object> suggestions(
            @RequestParam(name = "dorm_id", required = false) String dormId,
            @RequestParam(required = false) Integer floor,
            @RequestParam(name = "risk_level", required = false) String riskLevel,
            @RequestParam(name = "abnormal_type", required = false) String abnormalType,
            @RequestParam(name = "start_time", required = false) String startTime,
            @RequestParam(name = "end_time", required = false) String endTime,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(name = "page_size", defaultValue = "20") int pageSize
    ) {
        TeacherQuery query = new TeacherQuery(dormId, floor, riskLevel, abnormalType, startTime, endTime);
        return dataStore.paginate(dataStore.suggestionRecords(query), page, pageSize);
    }

    @GetMapping("/rankings/energy")
    public Map<String, Object> energyRanking(@RequestParam(defaultValue = "10") int limit) {
        return Map.of("data", dataStore.topDormsByEnergy(limit));
    }
}
