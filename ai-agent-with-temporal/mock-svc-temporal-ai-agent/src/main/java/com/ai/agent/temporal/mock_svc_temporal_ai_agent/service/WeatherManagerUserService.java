package com.ai.agent.temporal.mock_svc_temporal_ai_agent.service;

import com.ai.agent.temporal.mock_svc_temporal_ai_agent.response.WeatherManagerUserDetails;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class WeatherManagerUserService {

    private final Map<String, WeatherManagerUserDetails> weatherManagerUser =
            Map.of(
                    "UNITED STATES", new WeatherManagerUserDetails("Smith Johnson", "smithJohnson365"),
                    "UNITED KINGDOM", new WeatherManagerUserDetails("Emily Davis", "emilyDavis789"),
                    "FRANCE", new WeatherManagerUserDetails("Michael Brown", "michaelBrown456"),
                    "GERMANY", new WeatherManagerUserDetails("Olivia Wilson", "oliviaWilson123")
            );

    public WeatherManagerUserDetails getUserDetailsByCountry(String country){
        return weatherManagerUser.get(country.toUpperCase());
    }

}
