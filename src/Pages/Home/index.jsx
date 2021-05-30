import React, {useEffect, useMemo, useRef, useState} from "react";
import {ChatController, MuiChat} from "chat-ui-react";

function HomePage () {
  const [previousPrompts, setPreviousPrompts] = useState([])
  const inputRef = useRef()
  
  const [weather, setWeather] = useState('sunny') // sunny, windy, breezy, humid, dry
  const [season, setSeason] = useState('summer') // summer, winder, autumn, spring
  const [temperature, setTemperature] = useState(25) 
  const [crowd, setCrowd] = useState(5) // number of people around

  const [chatCtl] = useState(new ChatController());

  const dynamic = 'It is raining outside. The temperature is 21C. Date is May 29 2021. There are 15 persons looking at me.'
  const gpt3 = (input) => {
    let pastConversation = ''
    let index = 0
    const pastPrompts = Array.from(previousPrompts).reverse()
    for (const prompt of pastPrompts){
      index++
      if (index === 1){ 
        continue
      }
      if (prompt.sentBy === 'bot'){
        pastConversation = pastConversation + 'AI: ' + prompt.text + '\n'
      } else {
        pastConversation = pastConversation + 'Human: ' + prompt.text + '\n'
      }
      if (index > 10){
        break
      }
    }
    fetch(`https://5000-lime-otter-sr2efxd8.ws-eu08.gitpod.io/?input_text=${encodeURI(input)}&past_conversation=${encodeURI(pastConversation)}&dynamic=${encodeURI(dynamic)}`).then(async res => {
      return await res.json()
    }).then(async res => {
      let promptHistory = previousPrompts
      promptHistory.push({text: res.text, sentBy: 'bot'})
      await chatCtl.addMessage({
        type: 'text',
        content: res.text,
        self: false,
      });
      setPreviousPrompts(Array.from(promptHistory))
      chatCtl.setActionRequest({type: 'text'}).then(value => sendPrompt(value.value))
    })
  }
  
  const sendPrompt = async (input) => {
    let promptHistory = previousPrompts
    promptHistory.push({text: input, sentBy: 'me'})
    setPreviousPrompts(Array.from(promptHistory))
    gpt3(input)
    // inputRef.current.value = ''
  }

  useEffect(async () => {
    // Chat content is displayed using ChatController
    await chatCtl.addMessage({
      type: 'text',
      content: `Hello`,
      self: false,
    });
      chatCtl.setActionRequest({type: 'text'}).then(value => sendPrompt(value.value))
  }, []); 
  
  const handleKey = (e) => {
    if (e.key === 'Enter') {
      sendPrompt()
    }
  }
  
  
  return <>
    <div style={{width: '100%', paddingTop: '20px'}}>
      <img style={{width: '100px', height: 'auto'}} src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNkbniqOXYzXzaaQptg2tHEq2G7ep_BBSr-g&usqp=CAU"/>
    <h1>Talk to BЯYAN</h1>
    <br />
    <div style={{width: '400px', height: '500px', margin: 'auto', textAlign: 'start'}}>
      <MuiChat chatController={chatCtl} />
{/*    {previousPrompts.map((prompt, i) => {
      return <div key={i} style={{marginTop: '10px'}}>{prompt.sentBy === 'bot' ? <b>Brian: </b> : <b>You: </b>}{prompt.text}</div>
    })}*/} 
    </div> 
    <br/>
  {/*  <input ref={inputRef} onKeyDown={handleKey}/>
    <button style={{marginLeft: '6px', marginTop: '10px'}} onClick={sendPrompt}>Send</button>*/}
    </div>
  </>
}

export default HomePage