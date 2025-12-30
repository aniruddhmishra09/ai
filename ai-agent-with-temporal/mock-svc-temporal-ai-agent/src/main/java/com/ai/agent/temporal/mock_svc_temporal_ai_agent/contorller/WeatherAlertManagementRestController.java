package com.ai.agent.temporal.mock_svc_temporal_ai_agent.contorller;

import com.ai.agent.temporal.mock_svc_temporal_ai_agent.response.CountryApplicabilityDetails;
import com.ai.agent.temporal.mock_svc_temporal_ai_agent.response.WeatherManagerUserDetails;
import com.ai.agent.temporal.mock_svc_temporal_ai_agent.service.AlertManagementMasterService;
import com.ai.agent.temporal.mock_svc_temporal_ai_agent.service.WeatherManagerUserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/weather-alert-management")
@Slf4j
public class WeatherAlertManagementRestController {

    @Autowired
    private WeatherManagerUserService weatherManagerUserService;

    @Autowired
    private AlertManagementMasterService alertManagementMasterService;

    @GetMapping("/user-details/{country}")
    public ResponseEntity<WeatherManagerUserDetails> getUserDetails(@PathVariable( "country") String country) {
        log.info("User Details request received for country: {}", country);
        WeatherManagerUserDetails userDetails = weatherManagerUserService.getUserDetailsByCountry(country);
        if (userDetails != null) {
            log.info("User Details found: {}", userDetails);
            return ResponseEntity.ok(userDetails);
        } else {
            log.info("No User Details found for country: {}", country);
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/country-applicability/{country}")
    public ResponseEntity<CountryApplicabilityDetails> checkCountryApplicability(@PathVariable("country") String country) {
        log.info("Country Applicability request received for country: {}", country);
        boolean isApplicable = alertManagementMasterService.isCountryApplicable(country);
        log.info("Country: {} is applicable: {}", country, isApplicable);
        CountryApplicabilityDetails response = new CountryApplicabilityDetails(isApplicable);
        return ResponseEntity.ok(response);
    }







}
