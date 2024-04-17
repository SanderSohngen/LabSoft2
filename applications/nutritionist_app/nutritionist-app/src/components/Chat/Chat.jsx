import { useState, useMemo, useEffect } from "react";
import useWebSocket, { ReadyState } from 'react-use-websocket';
import {
    MainContainer,
    ChatContainer,
    ConversationHeader,
    Message,
    MessageInput,
    Avatar,
    MessageList
} from "@chatscope/chat-ui-kit-react";
import { useAuth } from '../../context/AuthContext';

function Chat( { patientName, patientId }) {
    const { user } = useAuth();
    const [messages, setMessages] = useState([]);
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const BASE_WS = BASE_URL.replace("http", "ws");

    const socketURL = useMemo(() => `${BASE_WS}ws/chat/${patientId}`);

    const { sendMessage, lastMessage, readyState } = useWebSocket(socketURL, {
        onOpen: () => sendMessage(user.access_token),
        shouldReconnect: () => true,
    });

    useEffect(() => {
        if (lastMessage !== null) {
            const receivedData = JSON.parse(lastMessage.data);
            const receivedMessage = {
                content: receivedData.content,
                timestamp: receivedData.timestamp,
                sender: receivedData.sender
            };
            setMessages(prevMessages => [...prevMessages, receivedMessage]);
        }
    }, [lastMessage]);

    const handleSend = (text) => {
        sendMessage(JSON.stringify({
            content: text,
            timestamp: new Date().toLocaleTimeString(),
            sender: user.name
        }));
    };

    const connectionStatus = {
        [ReadyState.CONNECTING]: "Conectando",
        [ReadyState.OPEN]: "Conectado",
        [ReadyState.CLOSING]: "Fechando",
        [ReadyState.CLOSED]: "Desconectado",
        [ReadyState.UNINSTANTIATED]: "Não inicializado"
    }[readyState];

    return (
        <MainContainer responsive style={{ height: "600px", width: "80%" }}>
          <ChatContainer style={{ display: "flex", flexDirection: "column", height: "100%" }}>
            <ConversationHeader>
                <ConversationHeader.Content userName={patientName} info={connectionStatus} />
            </ConversationHeader>
            <MessageList style={{ flexGrow: 1, minHeight: 0 }}>
                {messages.map((msg, index) => (
                    <Message
                        key={index}
                        model={{
                            message: msg.content,
                            sentTime: msg.timestamp,
                            sender: msg.sender,
                            direction: user.name === msg.sender ? "outgoing" : "incoming",
                        }}
                        avatarSpacer={!msg.avatar}
                        avatar={<Avatar name={msg.sender} />}
                    />
                ))}
            </MessageList>
            <MessageInput
                autoFocus
                placeholder="Digite aqui..."
                attachButton={false}
                onSend={handleSend}
            />
          </ChatContainer>
        </MainContainer>
    );
}

export default Chat;