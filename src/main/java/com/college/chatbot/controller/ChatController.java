package com.college.chatbot.controller;

import com.college.chatbot.dto.ChatRequest;
import com.college.chatbot.dto.ChatResponse;
import com.college.chatbot.service.ChatbotService;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*")
public class ChatController {

    private final ChatbotService chatbotService;

    public ChatController(ChatbotService chatbotService) {
        this.chatbotService = chatbotService;
    }

    @PostMapping
    public ChatResponse getBotResponse(@RequestBody ChatRequest request) {
        String message = request == null ? null : request.getMessage();
        String answer = chatbotService.processQuery(message);
        return new ChatResponse(answer);
    }
}