package com.ai.agent.temporal.mock_svc_temporal_ai_agent.service;

import com.ai.agent.temporal.mock_svc_temporal_ai_agent.response.WeatherReporterDetails;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class WeatherManagerUserService {

    private final Map<String, WeatherReporterDetails> weatherManagerUser =
            Map.of(
                    "UNITED STATES", new WeatherReporterDetails("Smith Johnson", "smithJohnson365"),
                    "UNITED KINGDOM", new WeatherReporterDetails("Emily Davis", "emilyDavis789"),
                    "FRANCE", new WeatherReporterDetails("Michael Brown", "michaelBrown456"),
                    "GERMANY", new WeatherReporterDetails("Olivia Wilson", "oliviaWilson123")
            );

    public WeatherReporterDetails getUserDetailsByCountry(String country){
        return weatherManagerUser.get(country.toUpperCase());
    }

}
