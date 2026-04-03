import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function ChatbotScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I am your AI Agri Advisor powered by Gemini. Ask me anything about farming.", isBot: true }
  ]);

  const handleSend = () => {
    if (!query.trim()) return;
    const userMessage = { id: Date.now(), text: query, isBot: false };
    setMessages(prev => [...prev, userMessage]);
    
    // Simulate Gemini delay
    setTimeout(() => {
      setMessages(prev => [...prev, { id: Date.now()+1, text: "Based on my analysis, applying organic compost can improve soil health significantly...", isBot: true }]);
    }, 1500);
    
    setQuery('');
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="p-4 border-b border-gray-100 flex-row items-center justify-between">
        <Text className="text-xl font-bold text-dark">Agri Advisor Gemini</Text>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text className="text-blue-500 font-medium">Close</Text>
        </TouchableOpacity>
      </View>

      <ScrollView className="flex-1 p-4 bg-gray-50">
        {messages.map(msg => (
          <View key={msg.id} className={`max-w-[80%] p-4 rounded-2xl mb-4 ${msg.isBot ? 'bg-purple-100 self-start rounded-tl-none' : 'bg-primary self-end rounded-tr-none'}`}>
            <Text className={`text-base ${msg.isBot ? 'text-purple-900' : 'text-white'}`}>{msg.text}</Text>
          </View>
        ))}
      </ScrollView>

      <View className="p-4 bg-white border-t border-gray-100 flex-row items-center">
        <TextInput
          className="flex-1 bg-gray-100 p-4 rounded-xl mr-3 text-dark"
          placeholder="Ask about crops, diseases..."
          value={query}
          onChangeText={setQuery}
        />
        <TouchableOpacity className="bg-purple-600 p-4 rounded-xl" onPress={handleSend}>
          <Text className="text-white font-bold">Send</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}
