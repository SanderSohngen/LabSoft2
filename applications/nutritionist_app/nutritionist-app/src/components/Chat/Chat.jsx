import {
    MainContainer,
    ChatContainer,
    ConversationHeader,
    Message,
    MessageInput,
    Avatar,
    MessageList
} from "@chatscope/chat-ui-kit-react";


function Chat( { user }) {
    const messages = [
        { content: "Hey, how are you Alice?", timestamp: "10:00 AM", sender: "Bob" },
        { content: "I'm good, thanks for asking!", timestamp: "10:01 AM", sender: "Alice" },
        { content: "Are you coming to the meeting tomorrow?", timestamp: "10:02 AM", sender: "Bob" },
        { content: "Yes, I'll be there.", timestamp: "10:03 AM", sender: "Alice" },
        { content: "Great, see you there!", timestamp: "10:05 AM", sender: "Bob" },
        { content: "What's the agenda?", timestamp: "10:06 AM", sender: "Alice" },
        { content: "Project planning and deadlines.", timestamp: "10:07 AM", sender: "Bob" },
        { content: "Understood, I'll prepare my notes.", timestamp: "10:09 AM", sender: "Alice" },
        { content: "Perfect, looking forward to your input.", timestamp: "10:15 AM", sender: "Bob" },
        { content: "Do we need to bring anything else?", timestamp: "10:16 AM", sender: "Alice" },
        { content: "Just make sure to review the last report.", timestamp: "10:18 AM", sender: "Bob" },
        { content: "Will do, thanks for the heads up.", timestamp: "10:20 AM", sender: "Alice" },
        { content: "No problem, see you tomorrow then.", timestamp: "10:21 AM", sender: "Bob" },
        { content: "See you!", timestamp: "10:22 AM", sender: "Alice" },
      ];
    return (
        <MainContainer responsive style={{ height: "600px", width: "80%" }}>
          <ChatContainer style={{ display: "flex", flexDirection: "column", height: "100%" }}>
            <ConversationHeader>
                <ConversationHeader.Content userName={user} />
            </ConversationHeader>
            <MessageList style={{ flexGrow: 1, minHeight: 0 }}>
                {messages.map( msg => (
                    <Message
                        key={msg.timestamp + msg.sender}
                        model={{
                        message: msg.content,
                        sentTime: msg.timestamp,
                        sender: msg.sender,
                        direction: user === msg.sender ? "incoming" : "outgoing",
                        }}
                        avatarSpacer={user !== msg.sender}
                        avatar={user === msg.sender ? <Avatar name={msg.sender} /> : null}
                    />
                ))}
            </MessageList>
            <MessageInput autoFocus placeholder="Digite aqui..." attachButton={false} />
          </ChatContainer>
        </MainContainer>
      );
    }

export default Chat;