package com.ai.agent.temporal.mock_svc_temporal_ai_agent.service;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AlertManagementMasterService {

    private final List<String> applicableCountries = List.of(
            "UNITED STATES",
            "UNITED KINGDOM",
            "FRANCE",
            "GERMANY"
    );
    public boolean isCountryApplicable(String country) {
        return applicableCountries.contains(country.toUpperCase());
    }
}
