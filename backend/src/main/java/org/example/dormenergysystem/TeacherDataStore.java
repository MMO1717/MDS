package org.example.dormenergysystem;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Predicate;
import java.util.stream.Collectors;

@Service
public class TeacherDataStore {
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final String configuredDataDir;

    private List<Map<String, Object>> dormRecords = List.of();
    private List<Map<String, Object>> abnormalRecords = List.of();
    private List<Map<String, Object>> floorLoadRecords = List.of();
    private List<Map<String, Object>> predictionRecords = List.of();
    private List<Map<String, Object>> suggestionRecords = List.of();

    public TeacherDataStore(@Value("${teacher.data-dir:}") String configuredDataDir) {
        this.configuredDataDir = configuredDataDir;
    }

    @PostConstruct
    public void reload() throws IOException {
        Path dataDir = resolveDataDir();
        dormRecords = load(dataDir, "dorm_energy_data.json");
        abnormalRecords = load(dataDir, "abnormal_list.json");
        floorLoadRecords = load(dataDir, "floor_load_data.json");
        predictionRecords = load(dataDir, "load_prediction_result.json");
        suggestionRecords = load(dataDir, "suggestion_data.json");
    }

    public Map<String, Object> overview() {
        String latestTime = dormRecords.stream()
                .map(record -> text(record, "time"))
                .max(String::compareTo)
                .orElse("");

        List<Map<String, Object>> latestRecords = dormRecords.stream()
                .filter(record -> Objects.equals(text(record, "time"), latestTime))
                .toList();

        double currentTotalPower = latestRecords.stream()
                .mapToDouble(record -> number(record, "power"))
                .sum();

        long currentAbnormalCount = latestRecords.stream()
                .filter(record -> Objects.equals(record.get("abnormal_status"), "abnormal"))
                .count();

        long currentHighRiskCount = latestRecords.stream()
                .filter(record -> Objects.equals(record.get("risk_level"), "高"))
                .count();

        double totalEnergy = latestEnergyByDorm().values().stream()
                .mapToDouble(Double::doubleValue)
                .sum();

        Map<String, Object> overview = new LinkedHashMap<>();
        overview.put("building", "A");
        overview.put("floor_count", 5);
        overview.put("dorm_count", dormRecords.stream().map(record -> text(record, "dorm_id")).filter(s -> !s.isBlank()).collect(Collectors.toSet()).size());
        overview.put("record_count", dormRecords.size());
        overview.put("latest_time", latestTime);
        overview.put("current_total_power", round(currentTotalPower));
        overview.put("total_energy", round2(totalEnergy));
        overview.put("current_abnormal_count", currentAbnormalCount);
        overview.put("current_high_risk_count", currentHighRiskCount);
        overview.put("abnormal_record_count", abnormalRecords.size());
        overview.put("suggestion_count", suggestionRecords.size());
        overview.put("risk_distribution", countBy(abnormalRecords, "risk_level"));
        overview.put("abnormal_type_distribution", countBy(abnormalRecords, "abnormal_type"));
        return overview;
    }

    public Map<String, Object> dashboard(int limit) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("overview", overview());
        result.put("floor_summary", floorSummary());
        result.put("top_energy_dorms", topDormsByEnergy(limit));
        return result;
    }

    public Map<String, Object> dormSummary(String dormId) {
        List<Map<String, Object>> records = dormRecords.stream()
                .filter(record -> Objects.equals(text(record, "dorm_id").toUpperCase(), dormId.toUpperCase()))
                .toList();

        if (records.isEmpty()) {
            throw new IllegalArgumentException("宿舍 " + dormId + " 不存在");
        }

        Map<String, Object> latest = records.stream()
                .max(Comparator.comparing(record -> text(record, "time")))
                .orElse(records.get(records.size() - 1));

        long abnormalCount = records.stream()
                .filter(record -> Objects.equals(record.get("abnormal_status"), "abnormal"))
                .count();

        double totalEnergy = records.stream()
                .mapToDouble(record -> number(record, "energy"))
                .max()
                .orElse(0);

        double avgPower = records.stream()
                .mapToDouble(record -> number(record, "power"))
                .average()
                .orElse(0);

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("dorm_id", dormId.toUpperCase());
        result.put("floor", latest.get("floor"));
        result.put("latest", latest);
        result.put("record_count", records.size());
        result.put("abnormal_count", abnormalCount);
        result.put("total_energy", round2(totalEnergy));
        result.put("avg_power", round(avgPower));
        return result;
    }

    public List<Map<String, Object>> floorSummary() {
        Map<Integer, Map<String, Object>> latestByFloor = new LinkedHashMap<>();
        for (Map<String, Object> record : floorLoadRecords) {
            Integer floor = intValue(record, "floor");
            if (floor == null) {
                continue;
            }
            Map<String, Object> old = latestByFloor.get(floor);
            if (old == null || text(record, "time").compareTo(text(old, "time")) > 0) {
                latestByFloor.put(floor, record);
            }
        }

        Map<Integer, Long> abnormalByFloor = abnormalRecords.stream()
                .map(record -> intValue(record, "floor"))
                .filter(Objects::nonNull)
                .collect(Collectors.groupingBy(floor -> floor, LinkedHashMap::new, Collectors.counting()));

        return latestByFloor.entrySet().stream()
                .sorted(Map.Entry.comparingByKey())
                .map(entry -> {
                    Map<String, Object> item = new LinkedHashMap<>(entry.getValue());
                    item.put("abnormal_count", abnormalByFloor.getOrDefault(entry.getKey(), 0L));
                    return item;
                })
                .toList();
    }

    public List<Map<String, Object>> topDormsByEnergy(int limit) {
        Map<String, Long> abnormalCounts = abnormalRecords.stream()
                .collect(Collectors.groupingBy(record -> text(record, "dorm_id"), LinkedHashMap::new, Collectors.counting()));

        return latestEnergyByDorm().entrySet().stream()
                .map(entry -> {
                    Map<String, Object> item = new LinkedHashMap<>();
                    item.put("dorm_id", entry.getKey());
                    item.put("energy", round2(entry.getValue()));
                    item.put("abnormal_count", abnormalCounts.getOrDefault(entry.getKey(), 0L));
                    return item;
                })
                .sorted((a, b) -> Double.compare(number(b, "energy"), number(a, "energy")))
                .limit(Math.max(1, limit))
                .toList();
    }

    public List<Map<String, Object>> dormRecords(TeacherQuery query) {
        return filter(dormRecords, query);
    }

    public List<Map<String, Object>> abnormalRecords(TeacherQuery query) {
        return filter(abnormalRecords, query);
    }

    public List<Map<String, Object>> floorLoadRecords(TeacherQuery query) {
        return filter(floorLoadRecords, query);
    }

    public List<Map<String, Object>> predictionRecords(TeacherQuery query) {
        return filter(predictionRecords, query);
    }

    public List<Map<String, Object>> suggestionRecords(TeacherQuery query) {
        return filter(suggestionRecords, query);
    }

    public Map<String, Object> paginate(List<Map<String, Object>> records, int page, int pageSize) {
        int safePage = Math.max(1, page);
        int safePageSize = Math.min(Math.max(1, pageSize), 200);
        int start = Math.min((safePage - 1) * safePageSize, records.size());
        int end = Math.min(start + safePageSize, records.size());

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("page", safePage);
        result.put("page_size", safePageSize);
        result.put("total", records.size());
        result.put("data", records.subList(start, end));
        return result;
    }

    private List<Map<String, Object>> filter(List<Map<String, Object>> source, TeacherQuery query) {
        List<Predicate<Map<String, Object>>> predicates = new ArrayList<>();

        Optional.ofNullable(query.dormId()).filter(s -> !s.isBlank()).ifPresent(dormId ->
                predicates.add(record -> text(record, "dorm_id").equalsIgnoreCase(dormId)));
        Optional.ofNullable(query.floor()).ifPresent(floor ->
                predicates.add(record -> Objects.equals(intValue(record, "floor"), floor)));
        Optional.ofNullable(query.riskLevel()).filter(s -> !s.isBlank()).ifPresent(riskLevel ->
                predicates.add(record -> Objects.equals(record.get("risk_level"), riskLevel)));
        Optional.ofNullable(query.abnormalType()).filter(s -> !s.isBlank()).ifPresent(abnormalType ->
                predicates.add(record -> Objects.equals(record.get("abnormal_type"), abnormalType)));
        Optional.ofNullable(query.startTime()).filter(s -> !s.isBlank()).ifPresent(startTime ->
                predicates.add(record -> text(record, "time").compareTo(startTime) >= 0));
        Optional.ofNullable(query.endTime()).filter(s -> !s.isBlank()).ifPresent(endTime ->
                predicates.add(record -> text(record, "time").compareTo(endTime) <= 0));

        return source.stream()
                .filter(record -> predicates.stream().allMatch(predicate -> predicate.test(record)))
                .toList();
    }

    private Path resolveDataDir() {
        List<Path> candidates = new ArrayList<>();
        if (configuredDataDir != null && !configuredDataDir.isBlank()) {
            candidates.add(Path.of(configuredDataDir));
        }
        candidates.add(Path.of("..", "algorithm", "算法端输出"));
        candidates.add(Path.of("algorithm", "算法端输出"));

        return candidates.stream()
                .map(Path::toAbsolutePath)
                .map(Path::normalize)
                .filter(Files::isDirectory)
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("找不到算法端输出目录，请检查 teacher.data-dir 配置"));
    }

    private List<Map<String, Object>> load(Path dataDir, String filename) throws IOException {
        Path path = dataDir.resolve(filename);
        return objectMapper.readValue(path.toFile(), new TypeReference<>() {});
    }

    private Map<String, Double> latestEnergyByDorm() {
        Map<String, Map<String, Object>> latest = new LinkedHashMap<>();
        for (Map<String, Object> record : dormRecords) {
            String dormId = text(record, "dorm_id");
            if (dormId.isBlank()) {
                continue;
            }
            Map<String, Object> old = latest.get(dormId);
            if (old == null || text(record, "time").compareTo(text(old, "time")) > 0) {
                latest.put(dormId, record);
            }
        }

        Map<String, Double> energy = new LinkedHashMap<>();
        latest.forEach((dormId, record) -> energy.put(dormId, number(record, "energy")));
        return energy;
    }

    private Map<String, Long> countBy(List<Map<String, Object>> records, String key) {
        return records.stream()
                .map(record -> text(record, key))
                .filter(value -> !value.isBlank())
                .collect(Collectors.groupingBy(value -> value, LinkedHashMap::new, Collectors.counting()));
    }

    private String text(Map<String, Object> record, String key) {
        Object value = record.get(key);
        return value == null ? "" : String.valueOf(value);
    }

    private double number(Map<String, Object> record, String key) {
        Object value = record.get(key);
        if (value instanceof Number number) {
            return number.doubleValue();
        }
        if (value == null || String.valueOf(value).isBlank()) {
            return 0;
        }
        return Double.parseDouble(String.valueOf(value));
    }

    private Integer intValue(Map<String, Object> record, String key) {
        Object value = record.get(key);
        if (value instanceof Number number) {
            return number.intValue();
        }
        if (value == null || String.valueOf(value).isBlank()) {
            return null;
        }
        return Integer.parseInt(String.valueOf(value));
    }

    private double round(double value) {
        return Math.round(value * 10.0) / 10.0;
    }

    private double round2(double value) {
        return Math.round(value * 100.0) / 100.0;
    }
}
