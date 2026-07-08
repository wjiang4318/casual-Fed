function NodeItem({node}: { node: { id: string; label: string; layer: number } }) {
  return (
    <li>{node.label}</li>
  );
}


export default async function Page() {
  {/* make the component async which lets us use await
    await fetch(url) sends the HTTP request and pauses until a response comes back. The result res is a response 
    object - metadata about the request 
    await res.json() reads the response body and parses it from json text into a real javascript object/array*/}
  const res = await fetch("http://127.0.0.1:8000/dag");
  const data = await res.json();
  const meetingRes = await fetch("http://127.0.0.1:8000/meetings/20260617");
  const meeting = await meetingRes.json();

  return (
    <div>
      <ul>
      {data.nodes.map((node) => (
        <NodeItem key={node.id} node={node} />
      ))}
      </ul>
      <p>{meeting.decision}</p>
      <p>{meeting.tone}</p>
      <p>{meeting.tone_confidence}</p>
      <p>{meeting.statement_text}</p>
    </div>
  );
}



