package org.example.dormenergysystem;

public record TeacherQuery(
        String dormId,
        Integer floor,
        String riskLevel,
        String abnormalType,
        String startTime,
        String endTime
) {
}
