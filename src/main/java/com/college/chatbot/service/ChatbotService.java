package com.college.chatbot.service;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

@Service
public class ChatbotService {

    private final Map<String, String> knowledgeBase = new HashMap<>();

    public ChatbotService() {
        knowledgeBase.put("admission", "Admissions open in June every year. Minimum eligibility is 60% in 10+2.");
        knowledgeBase.put("fees", "B.Tech fees is Rs. 75,000/semester. BCA fees is Rs. 40,000/semester.");
        knowledgeBase.put("hostel", "Hostel accommodation is available for both boys and girls with 24/7 Wi-Fi & mess.");
        knowledgeBase.put("placement", "Top recruiters: TCS, Infosys, Wipro, Amazon. Average package is Rs. 5.5 LPA.");
        knowledgeBase.put("timing", "College timing is 9:00 AM to 5:00 PM, Monday through Saturday.");
        knowledgeBase.put("library", "Library is open on weekdays from 8:00 AM to 8:00 PM.");
    }

    public String processQuery(String userQuery) {
        if (userQuery == null || userQuery.trim().isEmpty()) {
            return "Please type a valid question.";
        }

        String queryLower = userQuery.toLowerCase(Locale.ROOT);

        for (Map.Entry<String, String> entry : knowledgeBase.entrySet()) {
            if (queryLower.contains(entry.getKey())) {
                return entry.getValue();
            }
        }

        if (queryLower.matches(".*\\b(hi|hello|hey|namaste)\\b.*")) {
            return "Hello! I am your College Virtual Assistant. Ask me about admissions, fees, hostel, or placements.";
        }

        return "I am not sure about this yet. Please contact the administrative desk at admin@college.edu or call +91-XXXX-XXXXXX.";
    }
}