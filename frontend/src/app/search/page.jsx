import Card from "./(overview)/Card";

export default function Page({ searchParams }) {
  const movieName = searchParams?.q || " ";

  return (
    <div>
      <Card movieName={movieName} />
    </div>
  );
}
